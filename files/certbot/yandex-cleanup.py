#!/usr/bin/env python3

import os
import certbot_util

# Expected environment variables:
# CERTBOT_DOMAIN (domain.tld for *.domain.tld)
# YA_DNS_TOKEN

records = certbot_util.call_yandex_api(api_token=os.environ["YA_DNS_TOKEN"],
    call_method="GET", url="list", params={"domain": os.environ["CERTBOT_DOMAIN"]})["records"]

for record in records:
    if (record["type"] == "TXT") and (record["subdomain"] == "_acme-challenge"):
        record_id = record["record_id"]
        print("Deleting record {}".format(record_id))
        certbot_util.call_yandex_api(api_token=os.environ["YA_DNS_TOKEN"],
            call_method="POST", url="del", params={
                "domain"   : os.environ["CERTBOT_DOMAIN"],
                "record_id": record_id})

# dns1.yandex.ru, dns2.yandex.ru
certbot_util.wait_for_acme_records_deletion(domain=os.environ["CERTBOT_DOMAIN"],
    nameservers=["213.180.204.213", "93.158.134.213"])
