* https://github.com/cloudflare/cloudflare-go/releases
* https://support.cloudflare.com/hc/en-us/articles/360000841472

```shell
export CF_API_EMAIL=user@domain.tld
export CF_API_KEY=0000000000000000000000000000000000000
./flarectl user info
# List records
./flarectl dns list --zone domain.tld
# View record details
./flarectl dns list -zone domain.tld -id 00000000000000000000000000000000
# Add new record
# --ttl 1 means "auto"
./flarectl dns create -zone domain.tld --name test -content 0.0.0.0 --type A --ttl 900 --proxy no
```
