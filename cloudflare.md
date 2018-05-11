* https://github.com/cloudflare/cloudflare-go/releases
* https://support.cloudflare.com/hc/en-us/articles/360000841472

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
# --ttl 1 means "auto"
# add --proxy for new record's traffic to go through Cloundflare servers
./flarectl dns create -zone domain.tld --name test -content 0.0.0.0 --type A --ttl 900
# Delete a record
./flarectl dns delete --zone domain.tld --id 00000000000000000000000000000000
```
