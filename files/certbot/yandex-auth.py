import dns.resolver

google_resolver = dns.resolver.Resolver(configure=False)
google_resolver.nameservers = ["8.8.8.8"]
answer = google_resolver.query('_acme-challenge.chere.review', 'TXT')

print(str(answer[0]))
