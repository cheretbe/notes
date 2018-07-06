#!/usr/bin/env python3

import os
import pprint
import requests
import dns.resolver
import time

# Expected environment variables:
# CERTBOT_DOMAIN (domain.tld for *.domain.tld)
# CERTBOT_VALIDATION
# YA_DNS_TOKEN

api_url = "https://pddimp.yandex.ru/api2/admin/dns/"

def call_api(call_method, url, params={}):
    try:
        # https://tech.yandex.ru/pdd/doc/concepts/api-dns-docpage/
        reply = requests.request(call_method, api_url + url,
            params=params, headers={'PddToken': os.environ["YA_DNS_TOKEN"]})
        if reply.status_code != 200:
            raise Exception("Status code: {code} - {text}".format(code=reply.status_code, text=reply.text))
        reply_json = reply.json()
        if reply_json["success"] != "ok":
            raise Exception(reply_json["error"])
        return reply_json
    except Exception as e:
        raise Exception("Yandex API call error: {0}".format(str(e)))

call_api("POST", "add", {
    "domain"   : os.environ["CERTBOT_DOMAIN"],
    "type"     : "TXT",
    "subdomain": "_acme-challenge",
    "content"  : os.environ["CERTBOT_VALIDATION"],
    "ttl"      : 900})


google_resolver = dns.resolver.Resolver(configure=False)
# dns1.yandex.ru, dns2.yandex.ru
google_resolver.nameservers = ["213.180.204.213", "93.158.134.213"]

print('Waiting for DNS record with value "{}" to propagate'.format(os.environ["CERTBOT_VALIDATION"]))
for i in range(1, 20):
    found_record = False
    try:
        for record in google_resolver.query('_acme-challenge.{}'.format(os.environ["CERTBOT_DOMAIN"]), 'TXT'):
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
