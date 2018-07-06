### TODO
* Change renew logic
* Remove sleep in `yandex-cleanup.py`
* Add Cloudflare support

### Installation

```shell
add-apt-repository ppa:certbot/certbot
apt update
apt install certbot python3-pip
pip3 install dnspython
# comment out code in /etc/cron.d/certbot
```

### Notes

Run as ordinary user:
* `--config-dir` - default `/etc/letsencrypt/`
* `--logs-dir`   - default `/var/log/letsencrypt/`
* `--work-dir`   - default `/var/lib/letsencrypt/`

Source: https://certbot.eff.org/faq/#does-certbot-require-root-administrator-privileges
