* https://easyengine.io/tutorials/nginx/fail2ban/

```shell
apt install fail2ban
systemctl enable fail2ban --now
```

`/etc/fail2ban/jail.local` example
```
[DEFAULT]
ignoreip = 127.0.0.1/8 192.168.0.0/24 domain.tld
```

```shell
fail2ban-client status sshd
```
