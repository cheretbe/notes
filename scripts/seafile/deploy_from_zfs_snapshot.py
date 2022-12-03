#!/usr/bin/env python3

import os
import argparse
import subprocess


def main(args):
    print("Stopping containers")
    subprocess.check_call(
        ("docker", "compose", "stop"),
        cwd=args.compose_dir
    )

    # -H Do not print headers and separate fields by a single tab instead of arbitrary white space.
    # -p Display numbers in parsable (exact) values.
    last_snapshot = subprocess.check_output(
        (
            "zfs", "list", "-t", "snapshot", "-o", "name,creation", "-s", "creation",
            args.pool_name, "-Hp"
        ),
        text=True
    ).splitlines()[-1].split("\t")[0]
    print(f"Rolling back '{args.pool_name}' to the latest snapshot '{last_snapshot}'")
    subprocess.check_call(("zfs", "rollback", last_snapshot))

    # -o field A comma-separated list of columns to display, defaults to name,property,value,source.
    mount_point = subprocess.check_output(
        ("zfs", "get", "mountpoint", "-H", "-o", "value", args.pool_name),
        text=True
    ).rstrip()

    with open(
            os.path.join(mount_point, "!!!_warning_pool_info.txt"), "w", encoding="utf-8"
    ) as info_f:
        info_f.write(
            (
                f"This ZFS pool is rolled back on schedule by {os.path.realpath(__file__)} script.\n"
                "Any changes made here will be lost\n"
            )
        )

    print("Updating config")
    with open(
            os.path.join(mount_point, "data/seafile/conf/seahub_settings.py"), "r+", encoding="utf-8"
    ) as conf_f:
        # conf = conf_f.read()
        conf = conf_f.read().replace(parsed_args.source_url, parsed_args.mirror_url)
        conf_f.truncate()
        conf_f.write(conf)

    print("Starting containers")
    subprocess.check_call(
        ("docker", "compose", "start"),
        cwd=args.compose_dir
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # # Required positional argument
    # parser.add_argument("arg", help="Required positional argument")

    # # Optional argument flag which defaults to False
    # parser.add_argument("-f", "--flag", action="store_true", default=False)

    # # Optional argument which requires a parameter (eg. -d test)
    # parser.add_argument("-n", "--name", action="store", dest="name")

    # # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    # parser.add_argument(
    #     "-v",
    #     "--verbose",
    #     action="count",
    #     default=0,
    #     help="Verbosity (-v, -vv, etc)")

    # # Specify output of "--version"
    # parser.add_argument(
    #     "--version",
    #     action="version",
    #     version="%(prog)s (version {version})".format(version=__version__))

    parsed_args = parser.parse_args()
    parsed_args.pool_name = "hdd2/seafile_backup"
    parsed_args.compose_dir = "/opt/docker-configs/seafile/"
    parsed_args.source_url = "https://seafile.chere.one:50500"
    parsed_args.mirror_url = "https://seafile-mirror.chere.one"
    main(parsed_args)
