* https://github.com/cloudflare/cloudflare-go/releases
* https://support.cloudflare.com/hc/en-us/articles/360000841472
* https://api.cloudflare.com/#dns-records-for-a-zone-properties

```shell
# Flarectl
# https://github.com/cloudflare/cloudflare-go/blob/master/cmd/flarectl/README.md
export CF_API_EMAIL=user@domain.tld
export CF_API_KEY=0000000000000000000000000000000000000
./flarectl user info
# List records
./flarectl dns list --zone domain.tld
# View record details
./flarectl dns list -zone domain.tld -id 00000000000000000000000000000000
# Add a new record
# --ttl 1 means "auto" (default)
# add --proxy for new record's traffic to go through Cloundflare servers
./flarectl dns create -zone domain.tld --name test -content 0.0.0.0 --type A --ttl 900
# Delete a record
./flarectl dns delete --zone domain.tld --id 00000000000000000000000000000000
```

```shell
# Get zone ID by name ("result" item contains an array of objects that shoud 
# have attributes like {"name": "domain.tld", "id": "00000000000000000000000000000000"})
curl -X GET -H "X-Auth-Email: user@domain.tld" -H "X-Auth-Key: 0000000000000000000000000000000000000" https://api.cloudflare.com/client/v4/zones | json_pp

# Get DNS records
curl -X GET -H "X-Auth-Email: user@domain.tld" -H "X-Auth-Key: 0000000000000000000000000000000000000" https://api.cloudflare.com/client/v4/zones/00000000000000000000000000000000/dns_records | json_pp > domain_info.txt
```
