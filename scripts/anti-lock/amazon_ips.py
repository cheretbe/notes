#!/usr/bin/env python3

import sys
import os
import contextlib
import types
import argparse
import requests
import ipaddress

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(os.path.expanduser(filename), 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def main(args):
    amazon_nets = {}

    # https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html
    response = requests.get(
        "https://ip-ranges.amazonaws.com/ip-ranges.json"
    ).json()
    for prefix in response["prefixes"]:
        if int(prefix["ip_prefix"].split("/")[1]) <= args.min_net_size:
            if not amazon_nets.get(prefix["ip_prefix"]):
                amazon_nets[prefix["ip_prefix"]] = types.SimpleNamespace(
                    network=prefix["ip_prefix"],
                    ip_network=ipaddress.ip_network(prefix["ip_prefix"]),
                    comment=f"<auto Amazon> {prefix['service']} {prefix['region']}",
                    filtered=False
                )

    for amazon_netname, amazon_net in amazon_nets.items():
        for other_netname, other_net in amazon_nets.items():
            if (not amazon_net.filtered) and (not other_net.filtered) and (amazon_net != other_net):
                if amazon_net.ip_network.subnet_of(other_net.ip_network):
                    print(f"{amazon_net.ip_network} is a subnet of {other_net.ip_network}")
                    amazon_net.filtered = True
                if other_net.ip_network.subnet_of(amazon_net.ip_network):
                    print(f"{other_net.ip_network} is a subnet of {amazon_net.ip_network}")
                    other_net.filtered = True

    filtered_counter = 0
    unfiltered_counter = 0
    for amazon_netname, amazon_net in amazon_nets.items():
        if not amazon_net.filtered:
            unfiltered_counter += 1
            # print(amazon_netname)
        else:
            filtered_counter += 1
    print(unfiltered_counter, filtered_counter)

    sys.exit(0)

    with smart_open(filename=args.out_file) as output:
        for amazon_netname, amazon_net in amazon_nets.items():
            # print(amazon_net.network, amazon_net.comment, file=output)
            # if not (amazon_net.network.endswith("/32") or amazon_net.network.endswith("/24")):
            if True:
                print(
                    f':if ([:len [/ip firewall address-list find list="antilock-targets" and address="{amazon_net.network}"]] = 0) do={{\n'
                    f'  :put "Adding {amazon_net.network} ({amazon_net.comment}) to \'antilock-targets\'"\n'
                    f'  /ip firewall address-list add list=antilock-targets address={amazon_net.network} comment="{amazon_net.comment}"\n'
                    f'}}',
                    file=output
                )
    print(f"Total net count: {len(amazon_nets)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out_file", nargs="?", default=None, help="Output file name")
    parser.add_argument("-n", "--min-net-size", type=int, default=19, help="Min network size, default=19 (/19 = 8190 hosts)")
    main(args=parser.parse_args())
