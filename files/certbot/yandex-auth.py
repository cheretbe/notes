#!/usr/bin/env python3

import os
import certbot_util

# Expected environment variables:
# CERTBOT_DOMAIN (domain.tld for *.domain.tld)
# CERTBOT_VALIDATION
# YA_DNS_TOKEN

certbot_util.call_yandex_api(api_token=os.environ["YA_DNS_TOKEN"],
    call_method="POST", url="add", params={
        "domain"   : os.environ["CERTBOT_DOMAIN"],
        "type"     : "TXT",
        "subdomain": "_acme-challenge",
        "content"  : os.environ["CERTBOT_VALIDATION"],
        "ttl"      : 900})

# dns1.yandex.ru, dns2.yandex.ru
certbot_util.wait_for_acme_record(record_value=os.environ["CERTBOT_VALIDATION"],
    domain=os.environ["CERTBOT_DOMAIN"], nameservers=["213.180.204.213", "93.158.134.213"])
