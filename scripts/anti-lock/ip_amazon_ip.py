#!/usr/bin/env python3

import argparse
import ipaddress
import requests


def main(args):
    is_amazon_ip = False
    amazon_network = ""
    response = requests.get(
        "https://ip-ranges.amazonaws.com/ip-ranges.json"
    ).json()
    for prefix in response["prefixes"]:
        if int(prefix["ip_prefix"].split("/")[1]) <= args.min_net_size:
            if ipaddress.ip_address(args.ip) in ipaddress.ip_network(prefix["ip_prefix"]):
                amazon_network = f"{prefix['ip_prefix']} ({prefix['service']} {prefix['region']})"
                is_amazon_ip = True
                break
    if is_amazon_ip:
        print(f"Amazon network {amazon_network} contains address {args.ip}")
    else:
        print(f"Amazon IP ranges DO NOT contain address {args.ip}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("ip")
    parser.add_argument("-n", "--min-net-size", type=int, default=19, help="Min network size, default=19 (/19 = 8190 hosts)")

    args = parser.parse_args()
    main(args)