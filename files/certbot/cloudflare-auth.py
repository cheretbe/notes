#!/usr/bin/env python3

import os
import certbot_util

# Expected environment variables:
# CERTBOT_DOMAIN (domain.tld for *.domain.tld)
# CERTBOT_VALIDATION
# CF_API_EMAIL
# CF_API_KEY

#dummy = call_cloudflare_api(os.environ["CF_API_EMAIL"], os.environ["CF_API_KEY"], "get", "zones")

zone_id = certbot_util.cloudflare_get_zone_id(os.environ["CF_API_EMAIL"], os.environ["CF_API_KEY"], "chere.review")


certbot_util.call_cloudflare_api(os.environ["CF_API_EMAIL"], os.environ["CF_API_KEY"],
    "post", "zones/{}/dns_records".format(zone_id), params={
        "type": "TXT",
        "name": "test-2del",
        "content": "test-test-test",
        "proxied": False,
        "ttl": 1})
