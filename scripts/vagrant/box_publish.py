#!/usr/bin/env python3

# pylint: disable=invalid-name,missing-module-docstring,missing-function-docstring

import sys
import os
import argparse
import datetime
import pathlib
import subprocess
import requests
import questionary
import packaging.version

KNOWN_PROVIDERS = ["virtualbox", "libvirt"]


def normalize_routeros_version(version_str):
    """
    Normalize RouterOS version to ensure proper semantic versioning and return a Version object.

    RouterOS versions can be in formats like:
    - "7.12" -> "7.12.0"
    - "6.49.1" -> "6.49.1"
    - "7.12.1" -> "7.12.1"

    This ensures consistent version comparison.
    """
    parts = version_str.split(".")
    # Ensure we have at least major.minor.patch format
    while len(parts) < 3:
        parts.append("0")

    return packaging.version.Version(".".join(parts))


def ask_for_confirmation(prompt, batch_mode, default):
    if batch_mode:
        print(prompt)
        print(
            "Batch mode is on. Autoselecting default option ({})".format({True: "yes", False: "no"}[default])
        )
        confirmed = default
    else:
        confirmed = questionary.confirm(prompt, default=True).ask()
        if confirmed is None:  # Handle Ctrl+C
            confirmed = False
    if not confirmed:
        sys.exit(1)


def inc_version_release(new_base_version, current_version, separator):
    current_base_version, current_subversion = current_version.rsplit(separator, maxsplit=1)
    if current_base_version == new_base_version:
        new_version = current_base_version + separator + str(int(current_subversion) + 1)
    elif normalize_routeros_version(new_base_version) > normalize_routeros_version(current_base_version):
        new_version = new_base_version + separator + "0"
    else:
        sys.exit(
            f"Version to be released ({new_base_version}) is lower than currently "
            f"released ({current_base_version})"
        )
    return new_version


def detect_box_info(box_file):
    """Detect box name, provider, and base version from filename.

    Supports patterns: box-name_provider_version or box-name_version
    Returns (name, provider, version) with None for undetected values.
    """
    parts = pathlib.Path(box_file).stem.split("_")

    detected_version = None
    detected_provider = None

    if parts and all(c.isdigit() or c in ".-" for c in parts[-1]):
        detected_version = parts.pop()

    if parts and parts[-1] in KNOWN_PROVIDERS:
        detected_provider = parts.pop()

    detected_name = "_".join(parts) if parts else None

    return detected_name, detected_provider, detected_version


def select_box_file(batch_mode):
    box_files = sorted(pathlib.Path().rglob("*.box"))
    if len(box_files) == 0:
        sys.exit("Can't find any *.box files in current directory and subdirectories")
    if len(box_files) == 1:
        return str(box_files[0])
    if batch_mode:
        sys.exit("More than one box file has been found. Will not display selection " "dialog in batch mode")
    selected = questionary.select("Select a box file to publish", choices=[str(i) for i in box_files]).ask()
    if selected is None:
        sys.exit(1)
    return str(selected)


def check_vagrant_cloud_login(batch_mode):
    print("Checking Vagrant Cloud login...")

    if (
        subprocess.call(
            "vagrant cloud auth login --check",
            shell=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
        != 0
    ):
        print("You are not currently logged in.")
        sys.exit(
            "Set HCP_CLIENT_ID, HCP_CLIENT_SECRET env variables, "
            "use --hcp-client-id and --hcp-client-secret options or "
            "use --hcp-creds-prompt option for cloud auth to work"
        )


def get_box_description(batch_mode, is_new_box):
    box_description = ""
    if os.path.isfile("box_description.md"):
        print("Reading box description from 'box_description.md'")
        with open("box_description.md", "r") as desc_f:
            box_description = desc_f.read().strip("\n")

    # For a newly created box there has to be a description
    if is_new_box:
        if not box_description:
            if batch_mode:
                sys.exit(
                    "'box_description.md' is missing. Will not create a new box "
                    "without a description in batch mode"
                )
            box_description = questionary.text(
                "Please enter box description", default=box_description, multiline=True
            ).ask()
            if box_description is None:
                sys.exit(1)
    return box_description


def get_current_cloud_box_version(cloud_user_name, box_name):
    print("Getting currently released version info")
    response = requests.get(f"https://app.vagrantup.com/api/v1/box/{cloud_user_name}/{box_name}").json()
    if response.get("current_version", ""):
        current_version = response["current_version"]["version"]
        print(f"Currently released version of '{cloud_user_name}/{box_name}': {current_version}")
    else:
        print(f"There is no currently released version of '{cloud_user_name}/{box_name}'")
        current_version = ""
    return current_version, (response.get("message", "") == "box not found")


def get_version_description(box_file, batch_mode):
    description_md = pathlib.Path(box_file).with_suffix(".md")
    if description_md.exists():
        print(f"Reading version description from '{str(description_md)}'")
        with open(str(description_md), "r") as desc_f:
            version_description = desc_f.read().strip("\n")
    else:
        version_description = datetime.datetime.now().strftime("**%d.%m.%Y update**")

    if not batch_mode:
        version_description = questionary.text(
            "Please enter a version description", default=version_description, multiline=True
        ).ask()
        if version_description is None:
            sys.exit(1)

    return version_description


def publish_box(  # pylint: disable=too-many-arguments
    box_file,
    cloud_user_name,
    box_name,
    box_version,
    box_description,
    version_description,
    provider,
    dry_run_mode,
):
    print(f"Publishing '{box_file}' as '{cloud_user_name}/{box_name}'version {box_version}")
    vagrant_parameters = [
        "vagrant",
        "cloud",
        "publish",
        f"{cloud_user_name}/{box_name}",
        box_version,
        provider,
        box_file,
        "--version-description",
        version_description,
        "--release",
        "--force",
    ]
    if box_description:
        vagrant_parameters += ["--short-description", box_description]
    if dry_run_mode:
        print("Dry-run mode is on. Skipping vagrant cloud call")
        print(vagrant_parameters)
    else:
        subprocess.check_call(vagrant_parameters)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Publish boxes to Vagrant Cloud")
    parser.add_argument(
        "box_ver",
        nargs="?",
        default="",
        help="Box base version (optional, yyyymmdd will be used by default, where yyyy "
        "is current year, mm is current month, dd is current day)",
    )
    parser.add_argument("-f", "--box-file", default="", help="Path to a box file to publish")
    parser.add_argument(
        "-u",
        "--username",
        default="cheretbe",
        help="Vagrant Cloud user name (default: cheretbe)",
    )
    parser.add_argument(
        "-n",
        "--box-name",
        default="",
        help="Vagrant Cloud box name. Will try autodetection from box file name if not set",
    )
    parser.add_argument(
        "-s",
        "--version-separator",
        default=".",
        help="Separator. A character, that separates box base version from a box " "release (default: '.')",
    )
    parser.add_argument(
        "-b",
        "--batch",
        action="store_true",
        default=False,
        help="Batch mode (disables all interactive prompts)",
    )
    parser.add_argument(
        "--hcp-client-id",
        help="Hashicorp Cloud Portal client ID",
    )
    parser.add_argument(
        "--hcp-client-secret",
        help="Hashicorp Cloud Portal client secret",
    )
    parser.add_argument(
        "--hcp-creds-prompt",
        action="store_true",
        default=False,
        help="Prompt for Hashicorp Cloud Portal credentials interactively",
    )
    parser.add_argument(
        "-p",
        "--provider",
        choices=KNOWN_PROVIDERS,
        default=None,
        help="Box provider (virtualbox or libvirt). Will try autodetection from box file name if not set.",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        default=False,
        help=(
            "Dry run mode (doesn't actually publish a box, just echoes vagrant "
            "cloud command to be called)"
        ),
    )
    return parser.parse_args()


def main():
    options = parse_arguments()

    if options.hcp_creds_prompt:
        if options.batch:
            sys.exit("Cannot prompt for HCP credentials in batch mode")
        print("Enter Hashicorp Cloud Portal credentials")
        options.hcp_client_id = questionary.text("HCP client ID:").ask()
        if options.hcp_client_id is None:
            sys.exit(1)
        options.hcp_client_secret = questionary.password("HCP client secret:").ask()
        if options.hcp_client_secret is None:
            sys.exit(1)

    if options.box_file == "":
        options.box_file = select_box_file(batch_mode=options.batch)
    print(f"Box file name: {options.box_file}")
    if not pathlib.Path(options.box_file).is_file():
        sys.exit(f"File doesn't exist: {options.box_file}")
    cloud_user_name = options.username

    if options.hcp_client_id:
        os.environ["HCP_CLIENT_ID"] = options.hcp_client_id
    if options.hcp_client_secret:
        os.environ["HCP_CLIENT_SECRET"] = options.hcp_client_secret
    check_vagrant_cloud_login(options.batch)

    detected_name, detected_provider, detected_version = detect_box_info(options.box_file)

    box_name = options.box_name or detected_name
    box_version = options.box_ver or detected_version
    box_provider = options.provider or detected_provider

    if not box_name:
        if options.batch:
            sys.exit("Could not detect box name from file name in batch mode. Use --box-name option.")
        box_name = questionary.text("Box name:").ask()
        if box_name is None:
            sys.exit(1)

    if not box_version:
        box_version = datetime.datetime.now().strftime("%Y%m%d")
        if options.batch:
            print(f"Box version not specified or detected, using {box_version}")
        else:
            box_version = questionary.text("Box version:", default=box_version).ask()
            if box_version is None:
                sys.exit(1)

    if not box_provider:
        if options.batch:
            sys.exit("Could not detect provider from box file name in batch mode. Use --provider option.")
        box_provider = questionary.select(
            "Select box provider", choices=KNOWN_PROVIDERS, default=KNOWN_PROVIDERS[0]
        ).ask()
        if box_provider is None:
            sys.exit(1)

    print(f"Publishing '{cloud_user_name}/{box_name}' {box_version}")

    current_version, is_new_box = get_current_cloud_box_version(cloud_user_name, box_name)
    if current_version:
        new_version = inc_version_release(
            new_base_version=box_version,
            current_version=current_version,
            separator=options.version_separator,
        )
    else:
        new_version = box_version + options.version_separator + "0"

    box_description = get_box_description(batch_mode=options.batch, is_new_box=is_new_box)

    version_description = get_version_description(options.box_file, options.batch)

    current_version_info = ""
    if current_version:
        current_version_info = f", replacing currenly released version {current_version}"
    elif is_new_box:
        current_version_info = f", creating a new box\nNew box description: {box_description}"
    print(
        f"This will release '{options.box_file}' as '{cloud_user_name}/{box_name}' "
        f"version {new_version}" + current_version_info + f"\nVersion description: {version_description}"
    )
    ask_for_confirmation(prompt="Do you want to continue?", batch_mode=options.batch, default=True)

    publish_box(
        box_file=options.box_file,
        cloud_user_name=cloud_user_name,
        box_name=box_name,
        box_version=new_version,
        box_description=box_description,
        version_description=version_description,
        provider=box_provider,
        dry_run_mode=options.dry_run,
    )


if __name__ == "__main__":
    main()
