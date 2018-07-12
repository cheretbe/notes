import os
import requests
import json
import dns.resolver
import time

cloudflare_api_url = "https://api.cloudflare.com/client/v4/"

def call_cloudflare_api(email, api_key, call_method, url, data={}):
    # https://api.cloudflare.com/#dns-records-for-a-zone-properties
    try:
        reply = requests.request(call_method, cloudflare_api_url + url,
            data=json.dumps(data), headers={
                "X-Auth-Email": email,
                "X-Auth-Key":   api_key,
                "content-type": "application/json"})
        if reply.status_code != 200:
            raise Exception("Status code: {code} - {text}".format(code=reply.status_code, text=reply.text))
        reply_json = reply.json()
        if not reply_json["success"]:
            raise Exception(reply_json["errors"])
        return reply_json
    except Exception as e:
        raise Exception("Cloudflare API call error: {0}".format(repr(e)))

def cloudflare_get_zone_info(email, api_key, zone_name):
    zone_id = None
    name_servers = None
    for zone in call_cloudflare_api(email, api_key, "get", "zones")["result"]:
        if zone["name"] == zone_name:
            zone_id = zone["id"]
            name_servers = zone["name_servers"]
            break
    if not zone_id:
        raise Exception ("Cloudflare API error: Cannot find ID for zone {}".format(zone_name))
    return zone_id, name_servers

def dns_lookup(name, type="A", nameservers=None):
    if nameservers:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = nameservers
    else:
        resolver = dns.resolver
    return resolver.query(qname=name, rdtype=type)
