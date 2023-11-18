* https://github.com/cloudflare/cloudflare-go/releases
* https://support.cloudflare.com/hc/en-us/articles/360000841472
* https://api.cloudflare.com/#dns-records-for-a-zone-properties

```shell
# Flarectl
sudo snap install go --classic
export PATH=/snap/bin/go:$PATH
go install github.com/cloudflare/cloudflare-go/cmd/flarectl@latest
go/bin/flarectl --version

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
# Get zone ID by name ("result" item contains an array of objects that 
# have attributes like {"name": "domain.tld", "id": "00000000000000000000000000000000"})
curl -X GET -H "X-Auth-Email: user@domain.tld" -H "X-Auth-Key: 0000000000000000000000000000000000000" https://api.cloudflare.com/client/v4/zones | json_pp

# Get DNS records
curl -X GET -H "X-Auth-Email: user@domain.tld" -H "X-Auth-Key: 0000000000000000000000000000000000000" https://api.cloudflare.com/client/v4/zones/00000000000000000000000000000000/dns_records | json_pp > domain_info.txt
# Specific record ID
curl -X GET -H "X-Auth-Email: user@domain.com" -H "X-Auth-Key: 00000000" https://api.cloudflare.com/client/v4/zones/00000000/dns_records | jq -r '.result | map(select(.name=="host.domain.com")) | .[].id'

# [!!!] Names can be used for GET requests
https://api.cloudflare.com/client/v4/zones/?name=domain.tld
https://api.cloudflare.com/client/v4/zones/00000000000000000000000000000000/dns_records?type=A&name=host.domain.tld

# Update a record
curl -X PUT "https://api.cloudflare.com/client/v4/zones/00000000000000000000000000000000/dns_records/00000000000000000000000000000000" \
  -H "X-Auth-Email: user@domain.tld" \
  -H "X-Auth-Key: 000000000000000000000000000000000000000000000" \
  -H "Content-Type: application/json" \
  --data '{"type": "A", "name": "test.domain.tld", "content": "127.0.0.1", "ttl": 900, "proxied": false}'
```

### cloudflare-ddns

* https://github.com/favonia/cloudflare-ddns

### ddclient

* Decided against using it because it:<br>
    * contains bugs like this: https://github.com/ddclient/ddclient/issues/590
    * acts weirdly (`make install` overwrites `/etc/ddclient/ddclient.conf`, constant changes of attributest of `/etc/ddclient/ddclient.conf`, etc)
    * written in Perl :alien:
* Notes
    * https://github.com/ddclient/ddclient
    * https://www.davidschlachter.com/misc/cloudflare-ddclient
    * https://cloudflare.com/cdn-cgi/trace
    * Dependencies for building from source: `apt install make autoconf libplack-perl libhttp-daemon-ssl-perl libtest-mockmodule-perllibtest-warnings-perl`
