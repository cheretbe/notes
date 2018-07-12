#!/usr/bin/env python3

import os
import time
import certbot_util

# Expected environment variables:
# CERTBOT_DOMAIN (domain.tld for *.domain.tld)
# CERTBOT_VALIDATION
# CF_API_EMAIL
# CF_API_KEY

zone_id, name_servers = certbot_util.cloudflare_get_zone_info(email=os.environ["CF_API_EMAIL"],
    api_key=os.environ["CF_API_KEY"], zone_name=os.environ["CERTBOT_DOMAIN"])

name_server_ips = []
for name_server in name_servers:
    for record in certbot_util.dns_lookup(name=name_server):
        name_server_ips += [str(record)]

certbot_util.call_cloudflare_api(email=os.environ["CF_API_EMAIL"], api_key=os.environ["CF_API_KEY"],
    call_method="POST", url="zones/{}/dns_records".format(zone_id), data={
        "type": "TXT",
        "name": "_acme-challenge",
        "content": os.environ["CERTBOT_VALIDATION"],
        "proxied": False,
        "ttl": 1})

print('Waiting for DNS record with value "{}" to propagate'.format(os.environ["CERTBOT_VALIDATION"]))
for i in range(1, 20):
    found_record = False
    try:
        for record in certbot_util.dns_lookup(name='_acme-challenge.{}'.format(os.environ["CERTBOT_DOMAIN"]),
                type='TXT', nameservers=name_server_ips):
            print("  " + str(record))
            # TXT records are double-quoted
            if str(record).strip('"') == os.environ["CERTBOT_VALIDATION"]:
                found_record = True
                break
    except Exception as e:
        print(repr(e))
    print("Record was found: {} (attempt {} of {})".format(found_record, i, 20))
    if found_record:
        break
    time.sleep(10)
