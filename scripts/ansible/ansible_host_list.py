#!/usr/bin/env python3

import argparse
import subprocess
import json
import yaml


def main(args):
    host_list = []
    ansible_cmd = ["ansible", "-m", "ping", args.limit, "--list-hosts"]
    if args.inventory:
        ansible_cmd += ["-i", args.inventory]

    for line in subprocess.check_output(ansible_cmd).decode("utf-8").splitlines():
        if line.startswith("    "):
            host_list += [line[4:]]

    if args.output_format == "text":
        print(" ".join(host_list))
    elif args.output_format == "list":
        for host in host_list:
            print(host)
    elif args.output_format == "csv":
        print(",".join(host_list))
    elif args.output_format == "json":
        print(json.dumps(host_list, ensure_ascii=False, indent=4))
    elif args.output_format == "yaml":
        print(yaml.dump(host_list, default_flow_style=False))
    elif args.output_format == "menu":
        menu_items = [{"label": host, "text": host} for host in host_list]
        print(yaml.dump(menu_items, default_flow_style=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--inventory", dest="inventory")
    parser.add_argument("-l", "--limit", default="all")
    parser.add_argument(
        "-o", "--output-format", choices=["text", "list", "csv", "json", "yaml", "menu"], default="text"
    )

    args = parser.parse_args()
    main(args)
