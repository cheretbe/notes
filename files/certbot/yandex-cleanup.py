#!/usr/bin/env python3

import os
import requests
import time

# Expected environment variables:
# CERTBOT_DOMAIN (domain.tld for *.domain.tld)
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


records = call_api("GET", "list", {"domain": os.environ["CERTBOT_DOMAIN"]})["records"]
for record in records:
    if (record["type"] == "TXT") and (record["subdomain"] == "_acme-challenge"):
        record_id = record["record_id"]
        print("Deleting record {}".format(record_id))
        call_api("POST", "del", {
            "domain"   : os.environ["CERTBOT_DOMAIN"],
            "record_id": record_id})

# TODO: replace with DNS lookup in a loop to ensure that DNS server does not return any records
time.sleep(10)
