#!/usr/bin/env python3

import os
import pprint
import dns.resolver

# CERTBOT_DOMAIN (domain.tld for *.domain.tld)
# CERTBOT_VALIDATION
# os.environ["AO_DEFAULT_VM_USER_NAME"]

google_resolver = dns.resolver.Resolver(configure=False)
google_resolver.nameservers = ["8.8.8.8"]
answer = google_resolver.query('_acme-challenge.chere.review', 'TXT')

print(str(answer[0]))

pprint.pprint(vars(os.environ))
