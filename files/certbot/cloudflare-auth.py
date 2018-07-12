#!/usr/bin/env python3

import os
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

certbot_util.wait_for_acme_record(record_value=os.environ["CERTBOT_VALIDATION"],
    domain=os.environ["CERTBOT_DOMAIN"], nameservers=name_server_ips)
