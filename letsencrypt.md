
* https://github.com/acmesh-official/acme.sh/wiki/dnsapi#1-cloudflare-option
* https://developers.cloudflare.com/fundamentals/get-started/basic-tasks/find-account-and-zone-ids/

```shell
# API token summary
#   +--- Account name
#      +---domain.tld - Zone:Read, DNS:Edit

export CF_Token="sdfsdfsdfljlbjkljlkjsdfoiwje"
export CF_Account_ID="xxxxxxxxxxxxx"
export CF_Zone_ID="xxxxxxxxxxxxx"

# issuing
docker run --rm -it -v "$(pwd)/out":/acme.sh -e "CF_Token=$CF_Token" -e "CF_Account_ID=$CF_Account_ID" -e "CF_Zone_ID=$CF_Zone_ID" neilpang/acme.sh --issue --staging --dns dns_cf -d domain.tld -d "*.domain.tld" -d "*.rd.domain.tld"

# fixing attributes on host
docker run --rm  -it -v "$(pwd)/out":/acme.sh --entrypoint "/bin/chown" neilpang/acme.sh $(id -u):$(id -g) /acme.sh/domain.tld_ecc/domain.tld.key

# renewal
docker run --rm -it -v "$(pwd)/out":/acme.sh neilpang/acme.sh --renew --staging -d domain.tld -d "*.domain.tld" -d "*.rd.domain.tld"
```
