#!/usr/bin/env python3
"""
MikroTik Config Comparison Tool

Interactive script to compare MikroTik RouterOS configuration files.
"""

import argparse
import contextlib
import os
import subprocess
import sys
import tempfile
import typing
import pathlib
import questionary


@contextlib.contextmanager
def get_current_config(host: str):
    """
    Fetch current router config via SSH and yield a path to a temporary file.
    Deletes the file on exit.
    """
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".rsc")
    try:
        with os.fdopen(tmp_fd, "w") as tmp_file:
            print(f"\nReading config from {host} into {tmp_path}")
            subprocess.run(
                ["ssh", host, "/export terse show-sensitive"],
                stdout=tmp_file,
                check=True,
            )
        yield tmp_path
    finally:
        os.unlink(tmp_path)


def get_host_directories(base_dir: pathlib.Path) -> typing.List[str]:
    """
    Get sorted list of host directories from the MikroTik backups directory.
    """
    if not base_dir.exists():
        return []

    hosts = []
    for item in base_dir.iterdir():
        if item.is_dir():
            # Skip directories that do not contain any .rsc files
            if any(item.glob("*.rsc")):
                hosts.append(item.name)

    return sorted(hosts)


def get_rsc_files(host_dir: pathlib.Path):
    """
    Get list of .rsc files from a host backup directory.
    """

    rsc_files = []
    for item in host_dir.glob("*.rsc"):
        if item.is_file():
            rsc_files.append(item.name)

    return sorted(rsc_files)


def select_config_file(rsc_files: typing.List[str], prompt: str) -> str:
    """
    Interactively select a config file.
    """

    print("")
    return questionary.select(prompt, choices=rsc_files, default=rsc_files[len(rsc_files) - 1]).ask()


def compare_configs(config1: str, config2: str, compare_tool: str):
    """
    Compare two configs using the specified tool.
    """
    print(f"\n{'='*60}")
    print("Comparing")
    print(f"{'='*60}")
    print(f"Config 1: {config1}")
    print(f"Config 2: {config2}")
    print(f"Tool:     {compare_tool}\n")

    if compare_tool == "git":
        subprocess.run(
            ["git", "diff", "--no-index", "--color-words", config1, config2],
        )
    elif compare_tool == "meld":
        subprocess.run(
            ["meld", config1, config2],
        )
    elif compare_tool == "vscode":
        subprocess.run(
            ["code", "--new-window", "--diff", config1, config2, "--wait"],
        )


def parse_args():
    parser = argparse.ArgumentParser(description="MikroTik Config Comparison Tool")
    parser.add_argument(
        "-c",
        "--compare-tool",
        choices=["git", "meld", "vscode"],
        default="git",
        dest="compare_tool",
        help="Tool to use for comparison (default: git)",
    )
    return parser.parse_args()


def main(args):
    try:
        backup_dir = pathlib.Path.home() / "Documents" / "data" / "mikrotik"
        if not backup_dir.exists():
            raise Exception(f"MikroTik backup directory not found: {backup_dir}")

        hosts = get_host_directories(base_dir=backup_dir)
        if not hosts:
            raise Exception(f"No host directories found in {backup_dir}")

        # Select host
        print("\n" + "=" * 60)
        print("MikroTik Config Comparison Tool")
        print("=" * 60 + "\n")

        host = questionary.select("Select a host:", choices=hosts).ask()
        if host is None:
            return 1

        rsc_files = get_rsc_files(backup_dir / host)
        print(f"Found {len(rsc_files)} config(s)")

        config1 = select_config_file(rsc_files, "Select first config to compare:")
        if config1 is None:
            exit(1)

        config2 = select_config_file(
            ([f for f in rsc_files if f != config1] + ["Current router config"]),
            "Select second config to compare:",
        )

        if config2 == "Current router config":
            with get_current_config(host) as current_config:
                compare_configs(str(backup_dir / host / config1), current_config, args.compare_tool)
        else:
            compare_configs(
                str(backup_dir / host / config1), str(backup_dir / host / config2), args.compare_tool
            )

            return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main(parse_args()))
