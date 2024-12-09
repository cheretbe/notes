#!/usr/bin/env python3

import argparse
import requests
import yaml


def main(args):
    print("Reading IP list")

    response = requests.get(
        "https://stat.ripe.net/data/country-resource-list/data.json?resource=RU"
    ).json()

    with open(args.vars_file, "w") as vars_f:
        # default_flow_style=False generates human-readable text
        vars_f.write(yaml.dump({"ru_ips": response["data"]["resources"]["ipv4"]}, default_flow_style=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vars_file", help="Output ansible vars file")
    args = parser.parse_args()

    main(args)