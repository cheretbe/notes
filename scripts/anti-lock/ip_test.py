#!/usr/bin/env python3

import argparse
import ipaddress

# dig +short ya.ru | grep -v '\.$' | xargs -I % scripts/anti-lock/ip_test.py %

def main(args):
    # curl https://stat.ripe.net/data/country-resource-list/data.json?resource=RU | jq -r '.data.resources.ipv4 | .[]' > /tmp/ru_ip_list.txt
    with open("/tmp/ru_ip_list.txt", "r") as f:
        for line in f:
            ip_range = line.rstrip()
            if "-" in ip_range:
                first_ip, last_ip = ip_range.split("-")
                ip_networks = list(ipaddress.summarize_address_range(
                    first=ipaddress.IPv4Address(first_ip), last=ipaddress.IPv4Address(last_ip)
                ))
            else:
                ip_networks = [ipaddress.ip_network(ip_range)]
            for ip_network in ip_networks:
                if ipaddress.ip_address(args.ip) in ip_network:
                    print(f"{args.ip} is in {ip_network} network")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("ip")

    args = parser.parse_args()
    main(args)
