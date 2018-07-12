#!/usr/bin/env python3

import os
import time
import certbot_util

# Expected environment variables:
# CERTBOT_DOMAIN (domain.tld for *.domain.tld)
# CF_API_EMAIL
# CF_API_KEY

zone_id, name_servers = certbot_util.cloudflare_get_zone_info(email=os.environ["CF_API_EMAIL"],
    api_key=os.environ["CF_API_KEY"], zone_name=os.environ["CERTBOT_DOMAIN"])

name_server_ips = []
for name_server in name_servers:
    for record in certbot_util.dns_lookup(name=name_server):
        name_server_ips += [str(record)]

records = certbot_util.call_cloudflare_api(email=os.environ["CF_API_EMAIL"], api_key=os.environ["CF_API_KEY"],
    call_method="GET", url="zones/{}/dns_records".format(zone_id))["result"]

for record in records:
    if (record["type"] == "TXT") and (record["name"] == "_acme-challenge.{}".format(os.environ["CERTBOT_DOMAIN"])):
        record_id = record["id"]
        print("Deleting record {}".format(record_id))
        certbot_util.call_cloudflare_api(email=os.environ["CF_API_EMAIL"], api_key=os.environ["CF_API_KEY"],
            call_method="DELETE", url="zones/{}/dns_records/{}".format(zone_id, record_id))

print("Waiting for DNS record(s) deletion to propagate")
for i in range(1, 5):
    record_count = 0
    try:
        record_count = len(certbot_util.dns_lookup(name='_acme-challenge.{}'.format(os.environ["CERTBOT_DOMAIN"]),
            type='TXT', nameservers=name_server_ips))
    except:
        pass
    print("Record count: {} (attempt {} of {})".format(record_count, i, 5))
    if record_count == 0:
        break
    time.sleep(10)
