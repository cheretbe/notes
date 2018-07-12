### Installation

```shell
add-apt-repository ppa:certbot/certbot
apt update
apt install certbot python3-dnspython
# comment out code in /etc/cron.d/certbot
```

### Usage
Yandex DNS
```shell
export YA_DNS_TOKEN=0000000000000000000000000000000000000000000000000000
# Obtain initial certificate
notes/files/certbot/obtain.py domain.tld *.domain.tld
# Renew
notes/files/certbot/obtain.py --renew
```
Cloudflare
```shell
export CF_API_EMAIL=user@domain.tld
export CF_API_KEY=0000000000000000000000000000000000000
# Obtain initial certificate
notes/files/certbot/obtain.py domain.tld *.domain.tld --service cloudflare
# Renew
notes/files/certbot/obtain.py --renew --service cloudflare
```
### Notes

Run as ordinary user:
* `--config-dir` - default `/etc/letsencrypt/`
* `--logs-dir`   - default `/var/log/letsencrypt/`
* `--work-dir`   - default `/var/lib/letsencrypt/`

Source: https://certbot.eff.org/faq/#does-certbot-require-root-administrator-privileges
