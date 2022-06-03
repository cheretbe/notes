* https://github.com/anudeepND/pihole-unbound
* https://github.com/pi-hole/pi-hole/#one-step-automated-install

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
