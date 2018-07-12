import os
import requests
import json
import dns.resolver
import time

yandex_api_url     = "https://pddimp.yandex.ru/api2/admin/dns/"
cloudflare_api_url = "https://api.cloudflare.com/client/v4/"

def call_yandex_api(api_token, call_method, url, params={}):
    try:
        # https://tech.yandex.ru/pdd/doc/concepts/api-dns-docpage/
        reply = requests.request(call_method, yandex_api_url + url,
            params=params, headers={'PddToken': api_token})
        if reply.status_code != 200:
            raise Exception("Status code: {code} - {text}".format(code=reply.status_code, text=reply.text))
        reply_json = reply.json()
        if reply_json["success"] != "ok":
            raise Exception(reply_json["error"])
        return reply_json
    except Exception as e:
        raise Exception("Yandex API call error: {0}".format(str(e)))

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

def wait_for_acme_record(record_value, domain, nameservers):
    print('Waiting for DNS record with value "{}" to propagate'.format(record_value))
    for i in range(1, 20):
        found_record = False
        try:
            for record in dns_lookup(name='_acme-challenge.{}'.format(domain),
                    type='TXT', nameservers=nameservers):
                print("  " + str(record))
                # TXT records are double-quoted
                if str(record).strip('"') == record_value:
                    found_record = True
        except Exception as e:
            print(repr(e))
        print("Record was found: {} (attempt {} of {})".format(found_record, i, 20))
        if found_record:
            break
        time.sleep(10)

def wait_for_acme_records_deletion(domain, nameservers):
    print("Waiting for DNS record(s) deletion to propagate")
    for i in range(1, 5):
        record_count = 0
        try:
            record_count = len(certbot_util.dns_lookup(name='_acme-challenge.{}'.format(domain),
                type='TXT', nameservers=nameservers))
        except:
            pass
        print("Record count: {} (attempt {} of {})".format(record_count, i, 5))
        if record_count == 0:
            break
        time.sleep(10)
