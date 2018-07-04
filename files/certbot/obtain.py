#!/usr/bin/env python

import sys
import argparse
import subprocess

def main():
    exit_code = 0

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('domains', metavar='domain', nargs='+')
        parser.add_argument('-s', '--service', dest='service', default="yandex",
            choices=["yandex", "cloudflare"], help='DNS service (default: %(default)s)')
        parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False)
        options = parser.parse_args()

	try:
            which_cmd = "where" if sys.platform == "win32" else "which"
            subprocess.check_output([which_cmd, "certbot-auto"])
        except:
            raise Exception("certbot-auto was not found. Make sure it is on PATH (e.g. located in '~/bin')")

        print("Domains: {}".format(options.domains))
        print("DNS service: {}".format(options.service))

        certbot_cmd = "certbot-auto certonly --manual --preferred-challenges dns"
        if options.debug:
            certbot_cmd += (" --server https://acme-staging-v02.api.letsencrypt.org/directory "
                "--agree-tos --no-eff-email --register-unsafely-without-email")
        else:
            certbot_cmd += " --server https://acme-v02.api.letsencrypt.org/directory"

        for domain in options.domains:
            certbot_cmd += " -d {}".format(domain)

        if options.service == "yandex":
            certbot_cmd += " --manual-auth-hook yandex-auth.py --manual-cleanup-hook yandex-cleanup.py"
        else:
            certbot_cmd += " --manual-auth-hook cloudflare-auth.py --manual-cleanup-hook cloudflare-cleanup.py"

        print(certbot_cmd)
        subprocess.check_call(certbot_cmd, shell=True)

    except Exception as e:
        print("Unhandled exception:")
        print(e)
        exit_code = 1

    return exit_code

if __name__ == '__main__':
    exit(main())
