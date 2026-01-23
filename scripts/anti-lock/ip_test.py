#!/usr/bin/env python3

import argparse
import datetime
import ipaddress
import json
import os
import socket
import requests

# dig +short ya.ru | grep -v '\.$' | xargs -I % scripts/anti-lock/ip_test.py %


def get_ip_list():
    """Fetch IP list for RU and BY countries with local caching."""
    cache_dir = os.path.expanduser("~/.cache/npa-scripts")
    cache_file = os.path.join(cache_dir, "ips_ru_by.json")

    # Check if cache exists and is fresh (less than 24 hours old)
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache_data = json.load(f)

        cache_time = datetime.datetime.fromtimestamp(cache_data.get("timestamp", 0))
        if datetime.datetime.now() - cache_time < datetime.timedelta(hours=24):
            return cache_data["ip_list"]

    # Fetch fresh data from API
    ip_list = []
    for country_code in ("RU", "BY"):
        response = requests.get(
            f"https://stat.ripe.net/data/country-resource-list/data.json?resource={country_code}"
        ).json()
        ip_list += response["data"]["resources"]["ipv4"]

    # Save to cache
    os.makedirs(cache_dir, exist_ok=True)
    cache_data = {"timestamp": datetime.datetime.now().timestamp(), "ip_list": ip_list}
    with open(cache_file, "w") as f:
        json.dump(cache_data, f)

    return ip_list


def main(args):
    ip_list = get_ip_list()

    # Determine if host is an IP or needs DNS resolution
    ips_to_check = []
    try:
        # Try to parse as IP address
        ipaddress.ip_address(args.host)
        ips_to_check = [args.host]
    except ValueError:
        # Not an IP, resolve as DNS name
        try:
            addr_info = socket.getaddrinfo(args.host, None, socket.AF_INET)
            ips_to_check = list(set([addr[4][0] for addr in addr_info]))
            print(f"Resolved {args.host} to: {', '.join(ips_to_check)}")
        except socket.gaierror as e:
            print(f"Failed to resolve {args.host}: {e}")
            return

    for ip in ips_to_check:
        found = False
        for ip_range in ip_list:
            if "-" in ip_range:
                first_ip, last_ip = ip_range.split("-")
                ip_networks = list(
                    ipaddress.summarize_address_range(
                        first=ipaddress.IPv4Address(first_ip), last=ipaddress.IPv4Address(last_ip)
                    )
                )
            else:
                ip_networks = [ipaddress.ip_network(ip_range)]
            for ip_network in ip_networks:
                if ipaddress.ip_address(ip) in ip_network:
                    print(f"{ip} is in {ip_network} network")
                    found = True
                    break
        if not found:
            print(f"{ip} is not a RU/BY IP address")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("host")

    args = parser.parse_args()
    main(args)
