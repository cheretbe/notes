* https://docs.pi-hole.net/guides/dns/unbound/
    * https://blacklab.net/set-up-pi-hole-as-truly-self-contained-dns-resolver/
        * Set `cache-size=0` in `/etc/dnsmasq.d/09-pihole-overrides.conf` instead of directly modifying `01-pihole.conf` (this should prevent losing this setting on pi-hole update). Caching is already handled by the Unbound.
        * Uncheck `Use DNSSEC` in `Settings` > `DNS` > `Advanced DNS settings`. Again Unbound already does DNSSEC validation.
* https://github.com/anudeepND/pihole-unbound
* https://github.com/pi-hole/pi-hole/#one-step-automated-install
DNSSEC validation.
Use pi-hole as a resolver on pi-hole host itself. Edit `/etc/dhcpcd.conf`:
```
interface eth0
     # ...
     static domain_name_servers=127.0.0.1
```

```shell
# Static records
nano /etc/hosts
pihole restartdns
```
