* https://easyengine.io/tutorials/nginx/fail2ban/

```shell
apt install fail2ban
```

`/etc/fail2ban/jail.local` example
```
ignoreip = 127.0.0.1/8 192.168.0.0/24 domain.tld
```
