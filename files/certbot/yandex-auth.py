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
google_resolver.nameservers = ["8.8.8.8"]

print("Waiting for DNS record to propagate")
for i in range(1, 20):
    try:
        answer = google_resolver.query('_acme-challenge.{}'.format(os.environ["CERTBOT_DOMAIN"]), 'TXT')
        record_value = str(answer[0])
    except:
        record_value = ""
    #print(record_value, os.environ["CERTBOT_VALIDATION"])
    print("Current value: {} (attempt {} of {})".format(record_value, i, 20))
    # Remove double quotes
    if record_value.strip('"') == os.environ["CERTBOT_VALIDATION"]:
        break
    time.sleep(10)
