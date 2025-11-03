#!/usr/bin/env python3

import argparse
import subprocess
import json
import yaml
import sys


def extract_groups_and_hosts(args):
    """Extract unique groups and hosts from inventory data"""
    groups = set()
    hosts = set()

    ansible_cmd = ["ansible-inventory", "--list"]
    if args.inventory:
        ansible_cmd += ["-i", args.inventory]
    inventory_data = json.loads(subprocess.check_output(ansible_cmd).decode("utf-8"))

    # Get all groups and hosts
    for group_name, group_data in inventory_data.items():
        if group_name == "_meta":
            continue

        # Filter out "all" group
        if group_name != "all":
            groups.add(group_name)

        if isinstance(group_data, dict) and "hosts" in group_data:
            hosts.update(group_data["hosts"])

    # Also get hosts from _meta section
    if "_meta" in inventory_data and "hostvars" in inventory_data["_meta"]:
        hosts.update(inventory_data["_meta"]["hostvars"].keys())

    return sorted(hosts), sorted(groups)


def main(args):
    host_list, group_list = extract_groups_and_hosts(args)

    # Check if host count is 0 and fail if it is
    if len(host_list) == 0:
        print("Error: No hosts found in inventory", file=sys.stderr)
        sys.exit(1)

    # Combine groups and hosts for output based on --groups flag
    if args.groups:
        all_items = group_list + host_list
    else:
        all_items = host_list

    if args.output_format == "text":
        print(" ".join(all_items))
    elif args.output_format == "list":
        for item in all_items:
            print(item)
    elif args.output_format == "csv":
        print(",".join(all_items))
    elif args.output_format == "json":
        print(json.dumps(all_items, ensure_ascii=False, indent=4))
    elif args.output_format == "yaml":
        print(yaml.dump(all_items, default_flow_style=False))
    elif args.output_format == "menu":
        menu_items = [{"label": item, "text": item} for item in all_items]
        print(yaml.dump(menu_items, default_flow_style=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List Ansible inventory groups and hosts using ansible-inventory"
    )

    parser.add_argument(
        "-i",
        "--inventory",
        dest="inventory",
        help="Specify inventory host path or comma separated host list",
    )
    parser.add_argument(
        "-g",
        "--groups",
        action="store_true",
        help="Include groups in the output (default: hosts only)",
    )
    parser.add_argument(
        "-o",
        "--output-format",
        choices=["text", "list", "csv", "json", "yaml", "menu"],
        default="text",
        help="Output format for the results",
    )

    args = parser.parse_args()
    main(args)
