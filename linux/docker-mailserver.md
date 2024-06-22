### Docker Mailserver (DMS)
* https://github.com/docker-mailserver/docker-mailserver
* https://docker-mailserver.github.io/docker-mailserver/latest/config/advanced/override-defaults/postfix/

```shell
docker image inspect --format '{{ index .Config.Labels "org.opencontainers.image.version"}}' ghcr.io/docker-mailserver/docker-mailserver:latest
docker inspect --format '{{ index .Config.Labels "org.opencontainers.image.version"}}' ghcr.io/docker-mailserver/docker-mailserver mailserver

docker exec -ti mailserver setup help
docker exec -ti mailserver setup email list
docker exec -ti mailserver setup email add user@example.com [password]

docker exec -ti mailserver postconf -n

# [!] aliases
# https://docker-mailserver.github.io/docker-mailserver/latest/config/user-management/#about
# https://github.com/docker-mailserver/docker-mailserver/blob/master/docs/content/faq.md#how-can-i-configure-a-catch-all

# https://mailutils.org/manual/html_section/configuration.html
# https://mailutils.org/manual/html_section/SMTP-Mailboxes.html

# https://docker-mailserver.github.io/docker-mailserver/latest/config/environment/#logrotate_interval
# LOGROTATE_COUNT will be available v14.0.0

#/etc/postfix/master.cf
smtp      inet  n       -       y       -       -       smtpd
```
