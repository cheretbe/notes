#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess

def main():
    exit_code = 0

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('domains', metavar='domain', nargs='*')
        parser.add_argument('-s', '--service', dest='service', default="yandex",
            choices=["yandex", "cloudflare"], help='DNS service (default: %(default)s)')
        parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False)
        parser.add_argument('-r', '--renew', dest='renew', action='store_true', default=False)
        options = parser.parse_args()

        if (len(options.domains) == 0) and (not options.renew):
            raise Exception("At least one domain name must be specified when not using --renew")

        try:
            which_cmd = "where" if sys.platform == "win32" else "which"
            subprocess.check_output([which_cmd, "certbot"])
        except:
            raise Exception("certbot was not found. See README.md for details")

        if options.debug:
            workdir_root = os.path.expanduser("~/letsencrypt-staging")
        else:
            workdir_root = os.path.expanduser("~/letsencrypt")
        config_dir = os.path.join(workdir_root, "config")
        os.makedirs(config_dir, exist_ok=True)
        work_dir = os.path.join(workdir_root, "work")
        os.makedirs(work_dir, exist_ok=True)
        logs_dir = os.path.join(workdir_root, "log")
        os.makedirs(logs_dir, exist_ok=True)

        print("Domains: {}".format(options.domains))
        print("DNS service: {}".format(options.service))

        if options.renew:
            certbot_cmd = "certbot renew"
            if options.debug:
                certbot_cmd += " --dry-run"
        else:
            certbot_cmd = "certbot certonly --manual --preferred-challenges dns"
            if options.debug:
                certbot_cmd += (" --server https://acme-staging-v02.api.letsencrypt.org/directory "
                    "--agree-tos --no-eff-email --register-unsafely-without-email")
            else:
                certbot_cmd += " --server https://acme-v02.api.letsencrypt.org/directory"
            for domain in options.domains:
                certbot_cmd += " -d {}".format(domain)

        certbot_cmd += (" --config-dir {0} --logs-dir {1} --work-dir {2}".format(config_dir, logs_dir, work_dir))

        script_dir = os.path.dirname(os.path.realpath(__file__))
        if options.service == "yandex":
            auth_script = os.path.join(script_dir, "yandex-auth.py")
            cleanup_script = os.path.join(script_dir, "yandex-cleanup.py")
            needed_env_vars = ["YA_DNS_TOKEN"]
        else:
            auth_script = os.path.join(script_dir, "cloudflare-auth.py")
            cleanup_script = os.path.join(script_dir, "cloudflare-cleanup.py")
            needed_env_vars = ["CF_API_EMAIL", "CF_API_KEY"]
        certbot_cmd += " --manual-auth-hook {0} --manual-cleanup-hook {1}".format(auth_script, cleanup_script)

        not_set_vars = []
        for env_variable in needed_env_vars:
            if not os.environ.get(env_variable):
                not_set_vars.append(env_variable)
        if (not_set_vars):
            raise Exception("The following environment variable(s) are not set: {}".format(not_set_vars))

        print(certbot_cmd)
        #subprocess.check_call(certbot_cmd, shell=True)

    except Exception as e:
        print("Unhandled exception:")
        print(e)
        exit_code = 1

    return exit_code

if __name__ == '__main__':
    exit(main())
