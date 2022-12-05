#!/usr/bin/env python3

import os
import sys
import time
import argparse
import subprocess
import json
import pathlib
import shutil


def wait_for_container_health_status():
    print("Waiting for Docker container to become ready")
    start_time = time.time()
    while True:
        container_status = subprocess.check_output(
                ("docker", "inspect", "-f", "{{.State.Health.Status}}", "gitlab"),
                text=True
            ).rstrip()
        if container_status == "healthy":
            break
        if time.time() > (start_time + 600):
            sys.exit("ERROR: Timeout waiting for gitlab container to become ready (600s)")
        time.sleep(1)


def main(args):
    print("Getting current Docker image version")

    # --quiet, -q  Only display IDs
    gitlab_image_id = subprocess.check_output(
        ("docker", "compose", "images", "-q", "gitlab"),
        cwd=args.compose_dir,
        text=True
    ).rstrip()
    gitlab_image_info = json.loads(
        subprocess.check_output(
            ("docker", "inspect", gitlab_image_id),
            text=True
        )
    )
    # We are looking for tags like 'gitlab/gitlab-ce:15.5.4-ce.0'
    gitlab_image_tag = next(
        filter(lambda repo_tag: repo_tag.startswith("gitlab/gitlab-ce"), gitlab_image_info[0]["RepoTags"]),
        None
    )
    gitlab_version = gitlab_image_tag.split(":")[1].split("-")[0]
    print(f"Image version is {gitlab_version} ({gitlab_image_tag})")

    print("Getting the most recent backup info")
    # Backup files have names like '1670145039_2022_12_04_15.5.4_gitlab_backup.tar',
    # where the first part is Unix timestamp. We sort by this part and select the
    # last item.
    last_backup = sorted(
        pathlib.Path(parsed_args.backup_dir).glob("*.tar"),
        key=lambda file_name: int(file_name.stem.split("_", maxsplit=1)[0])
    )[-1]
    last_backup_gitlab_version = last_backup.stem.split("_")[4]
    print(f"Most recent backup is: {last_backup.name}")
    backup_file_to_restore = pathlib.Path(args.compose_data_dir) / "backups" / last_backup.name
    print(f"Copying backup to '{backup_file_to_restore}'")
    shutil.copy(last_backup, backup_file_to_restore)

    print("Copying config files")
    # -v increase verbosity
    # -r recurse into directories
    # -h output numbers in a human-readable format
    # -l copy symlinks as symlinks
    # -t preserve modification times
    subprocess.check_call((
        "/usr/bin/rsync", "-vrhlt",
        "/mnt/zfs-data/homemain-backup/mirror/gitlab/config/",
        "/opt/docker-data/gitlab/config"
    ))

    if gitlab_version == last_backup_gitlab_version:
        print("Container version doesn't need upgrading")
    else:
        print((
            "Upgrading container from version "
            f"{gitlab_version} to version {last_backup_gitlab_version}"
        ))
        print("Destroying gitlab container")
        subprocess.check_call(
            ("docker", "compose", "down"),
            cwd=args.compose_dir
        )
        print("Updating .env file")
        with open(
                os.path.join(args.compose_dir, ".env"), "r+", encoding="utf-8"
        ) as conf_f:
            # Backup file name doesn't contain full container version, so this
            # might potentially break when, for example, upgrading
            # from 9.5.3-ce.1 to 9.5.4-ce.0. Will fix this when we get there (will
            # probaly require querying Docker registry)
            conf = conf_f.read().replace(gitlab_version, last_backup_gitlab_version)
            conf_f.seek(0)
            conf_f.write(conf)
            conf_f.truncate()

        print("Saving current config")
        subprocess.check_call(
            (
                "docker compose -f docker-compose.yml -f docker-compose.local.yml"
                "config > local-data/config_$(date +%Y-%m-%d_%H-%M).txt"
            ),
            shell=True,
            cwd=args.compose_dir
        )

        print("Starting gitlab container")
        subprocess.check_call(
            ("docker", "compose", "-f", "docker-compose.yml", "-f", "docker-compose.local.yml", "up", "-d"),
            cwd=args.compose_dir
        )

        wait_for_container_health_status()

    print("Stopping Gitlab processes that are connected to the database")
    subprocess.check_call(("docker", "exec", "-it", "gitlab", "gitlab-ctl", "stop", "puma"))
    subprocess.check_call(("docker", "exec", "-it", "gitlab", "gitlab-ctl", "stop", "sidekiq"))

    print("Restoring backup")
    subprocess.check_call((
        "docker", "exec", "-it", "gitlab", "gitlab-backup", "restore",
        # '_gitlab_backup.tar' needs to be omitted
        ("BACKUP=" + last_backup.name.replace("_gitlab_backup.tar", "")),
        "force=yes"
    ))

    print("Restarting gitlab container")
    subprocess.check_call(
        ("docker", "compose", "restart"),
        cwd=args.compose_dir
    )
    wait_for_container_health_status()

    print("Running Gitlab self-check")
    subprocess.check_call((
        "docker", "exec", "-it", "gitlab", "gitlab-rake", "gitlab:check", "SANITIZE=true"
    ))

    # TODO:
    # - adjust name (maybe in compose file, make a comment here)
    # - disable backups
    # - monitor health? probably, yes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parsed_args = parser.parse_args()
    parsed_args.compose_dir = "/opt/docker-configs/gitlab"
    parsed_args.compose_data_dir = "/opt/docker-data/gitlab/data"
    parsed_args.compose_config_dir = "/opt/docker-data/gitlab/config"
    parsed_args.backup_dir = "/mnt/zfs-data/homemain-backup/mirror/gitlab/backups"
    parsed_args.backup_config_dir = "/mnt/zfs-data/homemain-backup/mirror/gitlab/config"
    main(parsed_args)
