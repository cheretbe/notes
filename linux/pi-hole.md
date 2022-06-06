* :point_right: Test: https://d3ward.github.io/toolz/adblock.html
* https://docs.pi-hole.net/guides/dns/unbound/
    * https://blacklab.net/set-up-pi-hole-as-truly-self-contained-dns-resolver/
        * Set `cache-size=0` in `/etc/dnsmasq.d/01-pihole.conf`. Caching is already handled by the Unbound. :warning: Check if this setting persists after pi-hole upgrade. Using override file like `09-pihole-overrides.conf` leads to "illegal repeated keyword" error :unamused:.
        * Uncheck `Use DNSSEC` in `Settings` > `DNS` > `Advanced DNS settings`. Again Unbound already does DNSSEC validation.
        * Also suggests more settings (see also https://github.com/anudeepND/pihole-unbound). :grey_question: compare with more authoritative source.
* https://github.com/pi-hole/pi-hole/#one-step-automated-install
DNSSEC validation.
Use pi-hole as a resolver on pi-hole host itself. Edit `/etc/dhcpcd.conf`:
```
interface eth0
     # ...
     static domain_name_servers=127.0.0.1
```
Change pi-hole PTR record: Add `PIHOLE_PTR=HOSTNAME` to `/etc/pihole/pihole-FTL.conf` (make sure to create `/etc/dnsmasq.d/09-lan-domain-tld.conf` file that contains `domain=lan.domain.tld` setting)

```shell
# Static records
nano /etc/hosts
pihole restartdns
```
