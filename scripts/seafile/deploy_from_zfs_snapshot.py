#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess
import pathlib
import json

# ./..
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import common #pylint: disable=import-error,wrong-import-position

def create_clone_dataset(pool_name, clone_name):
    # -H Do not print headers and separate fields by a single tab instead of arbitrary white space.
    # -p Display numbers in parsable (exact) values.
    # -S sorts by property in descending order.
    snapshots = subprocess.check_output(
        (
            "zfs", "list", "-t", "snapshot", "-o", "name,creation", "-S", "creation",
            pool_name, "-Hp"
        ),
        text=True
    ).splitlines()
    # filter @syncoid_* entries to avoid deletion problem during next sync
    # (we expect latest autosnap_* to last longer)
    latest_autosnap = None
    for snapshot in snapshots:
        # hdd2/seafile_backup@autosnap_2022-12-07_03:00:48_daily
        snapshot_name = snapshot.split("\t")[0]
        if snapshot_name.split("@")[1].startswith("autosnap_"):
            latest_autosnap = snapshot_name
            break

    clone_exists = True
    try:
        subprocess.check_call(
            ["zfs", "list", clone_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        clone_exists = False

    if clone_exists:
        print(f"Destroying existing clone '{clone_name}'")
        subprocess.check_call(["zfs", "destroy", clone_name])

    print(f"Cloning the latest snapshot '{latest_autosnap}' as '{clone_name}'")
    subprocess.check_call(["zfs", "clone", latest_autosnap, clone_name])

    # -o field A comma-separated list of columns to display, defaults to name,property,value,source.
    mount_point = subprocess.check_output(
        ("zfs", "get", "mountpoint", "-H", "-o", "value", clone_name),
        text=True
    ).rstrip()

    with open(
            os.path.join(mount_point, "!!!_warning_pool_info.txt"), "w", encoding="utf-8"
    ) as info_f:
        info_f.write(
            (
                f"This ZFS dataset is cloned on schedule by {os.path.realpath(__file__)} script.\n"
                "Any changes made here will be lost\n"
            )
        )
    return mount_point


def main(args):
    print("Getting current Docker image version")
    # --quiet, -q  Only display IDs
    gitlab_image_id = subprocess.check_output(
        ("docker", "compose", "images", "-q", "seafile"),
        cwd=args.compose_dir,
        text=True
    ).rstrip()
    seafile_image_info = json.loads(
        subprocess.check_output(
            ("docker", "inspect", gitlab_image_id),
            text=True
        )
    )
    current_docker_version = None
    for env_line in seafile_image_info[0]["Config"]["Env"]:
        env_var_name, env_var = env_line.split("=", maxsplit=1)
        if env_var_name == "SEAFILE_VERSION":
            current_docker_version = env_var
            break
    print(f"Current version: {current_docker_version}")

    print("Stopping containers")
    subprocess.check_call(
        ("docker", "compose", "stop"),
        cwd=args.compose_dir
    )

    mount_point = create_clone_dataset(pool_name=args.pool_name, clone_name=args.clone_name)

    print("Updating config")
    with open(
            os.path.join(mount_point, "data/seafile/conf/seahub_settings.py"), "r+", encoding="utf-8"
    ) as conf_f:
        # conf = conf_f.read()
        conf = conf_f.read().replace(parsed_args.source_url, parsed_args.mirror_url)
        conf_f.seek(0)
        conf_f.write(conf)
        conf_f.truncate()

    print("Getting backup Docker image version")
    backup_docker_version = None
    with open("/mnt/hdd2/seafile_backup/container_info.json", encoding="utf-8") as conf_f:
        config = json.load(conf_f)
        for env_line in config[0]["Config"]["Env"]:
            env_var_name, env_var = env_line.split("=", maxsplit=1)
            if env_var_name == "SEAFILE_VERSION":
                backup_docker_version = env_var
                break
    print(f"Backup version: {backup_docker_version}")

    if current_docker_version == backup_docker_version:
        print("Container version doesn't need upgrading")
        print("Starting containers")
        subprocess.check_call(
            ("docker", "compose", "start"),
            cwd=args.compose_dir
        )
    else:
        print((
            "Upgrading container from version "
            f"{current_docker_version} to version {backup_docker_version}"
        ))
        common.upgrade_compose_container_versions(
            compose_dir=args.compose_dir,
            version_maps=[
                [
                    f"SEAFILE_IMAGE_VERSION={current_docker_version}",
                    f"SEAFILE_IMAGE_VERSION={backup_docker_version}"
                ]
            ]
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parsed_args = parser.parse_args()
    parsed_args.pool_name = "hdd2/seafile_backup"
    parsed_args.clone_name = "hdd2/seafile_mirror_clone"
    parsed_args.compose_dir = "/opt/docker-configs/seafile/"
    parsed_args.source_url = "https://seafile.chere.one:50500"
    parsed_args.mirror_url = "https://seafile-mirror.chere.one"
    main(parsed_args)
