https://about.gitlab.com/downloads/

#### Unsorted

* Fail2ban: https://gist.github.com/pawilon/238c278d3c6c4669771eb81b03264acd

### Installation

Install packages
```shell
# Prerequisites
sudo apt-get install curl openssh-server ca-certificates postfix
# Add repository and install the package
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
sudo apt-get install gitlab-ce
```

To store git data in and alternative directory adjust `git_data_dir` parameter in `/etc/gitlab/gitlab.rb`
```
git_data_dir "/var/opt/gitlab/git-data"
```
https://gitlab.com/gitlab-org/omnibus-gitlab/blob/629def0a7a26e7c2326566f0758d4a27857b52a3/README.md#storing-git-data-in-an-alternative-directory

Configure and start GitLab
```
sudo gitlab-ctl reconfigure
```
* Visit server URL in a web browser and set password for the user `root`
* Disable sign-up: Admin area > Settings (under the gear button) > Sign-up Restrictions > Sign-up enabled
* Add users without email: https://stackoverflow.com/questions/29704546/gitlab-signup-users-without-email-conformation/34525936#34525936

### Backup/restore
```
# limit backup lifetime to 7 days - 604800 seconds
gitlab_rails['backup_keep_time'] = 604800
```
```
gitlab-ctl reconfigure
/opt/gitlab/bin/gitlab-rake gitlab:backup:create
/opt/gitlab/bin/gitlab-rake gitlab:backup:create CRON=1
```
Default path is `/var/opt/gitlab/backups`

* https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/raketasks/backup_restore.md
```shell
# View available version
apt-cache policy gitlab-ce
# Install specific version
apt install -s gitlab-ce=12.3.3-ce.0
```

### Reverse proxy
Settings for `/etc/gitlab/gitlab.rb` on Gitlab server:
```ruby
external_url 'https://yourdomain.com'
nginx['listen_port'] = 80
nginx['listen_https'] = false
nginx['proxy_set_headers'] = {
  "X-Forwarded-Proto" => "https",
  "X-Forwarded-Ssl" => "on"
}

# https://docs.gitlab.com/omnibus/settings/nginx.html#configuring-gitlab-trusted_proxies-and-the-nginx-real_ip-module
nginx['real_ip_header'] = 'X-Real-IP'
nginx['real_ip_recursive'] = 'on'
gitlab_rails['trusted_proxies'] = ["192.168.0.1"]
```
Set `nginx['hsts_max_age'] = 0` if the proxy uses `add_header Strict-Transport-Security` to set HSTS (to avoid this header being added twice)

On the proxy use `location` settings for Nginx from here:
https://gitlab.com/gitlab-org/gitlab-recipes/blob/master/web-server/nginx/gitlab-omnibus-ssl-nginx.conf

```shell
# Apply changes
gitlab-ctl reconfigure
```

References
* https://gitlab.com/gitlab-org/gitlab-ce/issues/15574#note_12468383
* https://gist.github.com/sameersbn/becd1c976c3dc4866ef8

### SSL with Let's Encrypt certificate
```
sudo mkdir -p /var/www/letsencrypt
```
Add the following line to `/etc/gitlab/gitlab.rb`:
```
nginx['custom_gitlab_server_config']="location ^~ /.well-known/acme-challenge {\n alias /var/www/letsencrypt;\n}\n"
```
Reconfigure gitlab instance to activate new configuration
```
sudo gitlab-ctl reconfigure
```
```shell
sudo adduser --disabled-password letsencrypt
sudo chown letsencrypt: /var/www/letsencrypt
sudo cp letsencrypt-account.key /home/letsencrypt/
sudo chown letsencrypt:letsencrypt /home/letsencrypt/letsencrypt-account.key
sudo chmod 600 /home/letsencrypt/letsencrypt-account.key

# by analogy with /etc/ssl structure
sudo mkdir -p /etc/gitlab/ssl/certs
sudo chmod 755 /etc/gitlab/ssl/certs
sudo chown letsencrypt: /etc/gitlab/ssl/certs/
sudo mkdir /etc/gitlab/ssl/private
sudo chown :ssl-cert /etc/gitlab/ssl/private
sudo chmod 700 /etc/gitlab/ssl/private

openssl genrsa 4096 | sudo tee /etc/gitlab/ssl/private/example.com.key > /dev/null
sudo openssl req -new -sha256 -key /etc/gitlab/ssl/private/example.com.key -subj "/CN=example.com" -out /etc/gitlab/ssl/certs/example.com.csr

sudo su - letsencrypt

echo works > /var/www/letsencrypt/test.txt
curl example.com/.well-known/acme-challenge/test.txt
rm /var/www/letsencrypt/test.txt

git clone https://github.com/diafygi/acme-tiny.git
python3 acme-tiny/acme_tiny.py --account-key /home/letsencrypt/letsencrypt-account.key --csr /etc/gitlab/ssl/certs/example.com.csr --acme-dir /var/www/letsencrypt/ > /etc/gitlab/ssl/certs/ecample.com.pem

wget https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem -O /home/letsencrypt/lets-encrypt-x3-cross-signed.pem
cat /etc/gitlab/ssl/certs/example.com.pem /home/letsencrypt/lets-encrypt-x3-cross-signed.pem > /etc/gitlab/ssl/certs/example.com.fullchain.pem
```

Edit `/etc/gitlab/gitlab.rb`
```
external_url 'https://your_domain'
...
nginx['redirect_http_to_https'] = true
...
nginx['ssl_certificate'] = "/etc/letsencrypt/live/your_domain/fullchain.pem"
nginx['ssl_certificate_key'] = "/etc/letsencrypt/live/your_domain/privkey.pem"
```

activate new configuration
```
sudo gitlab-ctl reconfigure
```
* \[!\] https://scotthelme.co.uk/setting-up-le/
* https://thelinuxexperiment.com/automating-lets-encrypt-certificates-on-nginx/
* https://stosb.com/blog/secure-your-letsencrypt-setup-with-acme-tiny/
* https://webnugget.de/setting-up-gitlab-with-free-ssl-certs-from-lets-encrypt-on-ubuntu-14-04/
* https://www.digitalocean.com/community/tutorials/how-to-secure-gitlab-with-let-s-encrypt-on-ubuntu-16-04
* http://serverfault.com/questions/259302/best-location-for-ssl-certificate-and-private-keys-on-ubuntu
