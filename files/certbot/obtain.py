#!/usr/bin/env python

import argparse

def main():
    exit_code = 0

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('domains', metavar='domain', nargs='+')
        parser.add_argument('-s', '--service', dest='service', default="yandex",
            choices=["yandex", "cloudflare"], help='DNS service (default: %(default)s)')
        parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False)
        options = parser.parse_args()

        print("Domains: {}".format(options.domains))
        print("DNS service: {}".format(options.service))
        print("Debug: {}".format(options.debug))

    except Exception as e:
        print("Unhandled exception:")
        print(e)
        exit_code = 1

    return exit_code

if __name__ == '__main__':
    exit(main())
