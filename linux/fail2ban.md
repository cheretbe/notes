* https://easyengine.io/tutorials/nginx/fail2ban/

```shell
apt install fail2ban
systemctl enable fail2ban --now

cat /etc/fail2ban/jail.local
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

`/etc/fail2ban/jail.local` example
```
[DEFAULT]
ignoreip = 127.0.0.1/8 192.168.0.0/24 domain.tld
banaction = ufw
```

```shell
fail2ban-client reload

fail2ban-client status sshd
tail -f /var/log/fail2ban.log
```
