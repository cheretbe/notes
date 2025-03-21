https://about.gitlab.com/downloads/

#### Unsorted

* Fail2ban: https://gist.github.com/pawilon/238c278d3c6c4669771eb81b03264acd
* Display pipeline variables: https://gitlab.com/gitlab-org/gitlab/-/issues/22204

### Config

* gitlab.rb template
    * https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/files/gitlab-config-template/gitlab.rb.template
    * 16.11: https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/16-11-stable/files/gitlab-config-template/gitlab.rb.template

### Maintenance
* https://docs.gitlab.com/ee/administration/maintenance_mode/
    * WebUI version works only for activated EE
    * https://github.com/Lakr233/GitLab-License-Generator
```shell
gitlab-rails console
::Gitlab::CurrentSettings.update!(maintenance_mode_message: "New message")
::Gitlab::CurrentSettings.update!(maintenance_mode: true)
# API
curl --request PUT --header "PRIVATE-TOKEN:$ADMIN_TOKEN" "<gitlab-url>/api/v4/application/settings?maintenance_mode=true"
# Message text: maintenance_mode_message (try to determine the syntax for text with spaces)
# https://docs.gitlab.com/ee/api/settings.html
```

* [Investigating Sidekiq queue backlogs or slow performance](https://docs.gitlab.com/ee/administration/sidekiq/sidekiq_troubleshooting.html#investigating-sidekiq-queue-backlogs-or-slow-performance)

### API
* GraphQL
    * http://gitlab.domain.tld//-/graphql-explorer
    * https://docs.gitlab.com/ee/api/graphql/getting_started.html#queries-and-mutations
 
```
{
  runners(paused: true) {
		nodes {
      description
    }
  }
}

{
  runners(first: 100, search: "linux-gitlab-ci-medium") {
    nodes {
      id
      description
      shortSha
    }
    pageInfo {
      endCursor
      startCursor
      hasNextPage
    }
  }
}
```

### Installation

* https://about.gitlab.com/install/#ubuntu
* https://docs.gitlab.com/ee/administration/reference_architectures/1k_users.html

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

* Configure and start GitLab
    * :warning: Running GitLab in a memory-constrained environment: https://docs.gitlab.com/omnibus/settings/memory_constrained_envs.html
    * less dramatic optimizations: https://docs.gitlab.com/omnibus/settings/rpi.html#reduce-running-processes
```
sudo gitlab-ctl reconfigure
```
* Visit server URL in a web browser and set password for the user `root`
* Disable sign-up: Admin area > Settings (under the gear button) > Sign-up Restrictions > Sign-up enabled
* Add users without email: https://stackoverflow.com/questions/29704546/gitlab-signup-users-without-email-conformation/34525936#34525936
* Custom password length limits
    * `cd /opt/gitlab/embedded/service/gitlab-rails/config/initializers`
    * `cp devise_password_length.rb.example devise_password_length.rb`
    * Edit `config.password_length` parameter
    * Restart Gitlab
    * https://docs.gitlab.com/ee/security/password_length_limits.html

#### Docker
* https://github.com/cheretbe/docker-configs/tree/main/gitlab
    * :point_right: detailed config description is there, including `gitlab-ctl show-config` usage.
    * **TODO:** consider moving relevant content from `docker-configs/*/README.md` to notes and protecting main branch

#### Updgrade
* https://docs.gitlab.com/ee/update/index.html#upgrade-paths
* https://hub.docker.com/r/gitlab/gitlab-ce/tags
* https://docs.gitlab.com/ee/update/plan_your_upgrade.html#pre-upgrade-and-post-upgrade-checks
* https://docs.gitlab.com/ee/install/docker.html#upgrade

```
Refer to the GitLab Upgrade recommendations when upgrading between major versions.
  https://docs.gitlab.com/ee/update/index.html#upgrading-to-a-new-major-version
https://docs.gitlab.com/ee/update/plan_your_upgrade.html#pre-upgrade-and-post-upgrade-checks
Make full backup (not created automatically, make sure to include /etc/gitlab/)
Pull the new image
Stop the container
Create the container once again
On the first run, GitLab will reconfigure and upgrade itself.
```

### Backup/restore
* :warning: Make sure config files from `/etc/gitlab/` are backed up separately (https://gitlab.com/gitlab-org/gitlab-foss/-/blob/master/doc/raketasks/backup_gitlab.md#storing-configuration-files)
    * :point_right: Review recommendations here while implementing rundeck task: https://docs.gitlab.com/omnibus/settings/backups.html#creating-backups-for-gitlab-instances-in-docker-containers
    * `gitlab-ctl backup-etc` creates tar archive in `config_backup` subdir. Probably it't better to use `-p, --backup-path` and write to a separate backup mount as proposed in recommendations above
* :warning: Default commented value **is not** the default (default is to keep all backups). See https://gitlab.com/gitlab-org/gitlab/-/issues/17929.
```ruby
# limit backup lifetime to 7 days - 604800 seconds
gitlab_rails['backup_keep_time'] = 604800
```
```shell
gitlab-ctl reconfigure

# GitLab 12.2 or later
sudo gitlab-backup create
# The CRON=1 environment setting directs the backup script to hide all progress
# output if there aren't any errors. This is recommended to reduce cron spam.
# When troubleshooting backup problems, however, replace CRON=1 with --trace to log verbosely.
/opt/gitlab/bin/gitlab-backup create CRON=1

# GitLab 12.1 and earlier
#/opt/gitlab/bin/gitlab-rake gitlab:backup:create
#/opt/gitlab/bin/gitlab-rake gitlab:backup:create CRON=1
```
Default path is `/var/opt/gitlab/backups`

* https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/raketasks/backup_restore.md
```shell
# View available version
apt-cache policy gitlab-ce
# Install specific version
apt install -s gitlab-ce=12.3.3-ce.0
```
* Restoration gotchas
    * `gitlab-backup restore` searches for .tar files in `/var/opt/gitlab/backups`
    * `Restoring PostgreSQL database gitlabhq_production ... ERROR:  must be owner of extension pg_trgm` messages are harmless: https://forum.gitlab.com/t/gitlab-restore-backup-error/57131
    * when restoring to a temporary location like Docker container, adjust `external_url` and `proxy_set_headers` accordingly

#### Restore to Docker container

```shell
sudo cp /backup/source/1668535228_2022_11_15_14.8.2_gitlab_backup.tar /opt/docker-data/gitlab/data/backups/
sudo chown "$(docker exec gitlab id git -u):$(docker exec gitlab id git -g)" /opt/docker-data/gitlab/data/backups/1668535228_2022_11_15_14.8.2_gitlab_backup.tar

sudo cp /backup/source/gitlab-secrets.json /opt/docker-data/gitlab/config/
sudo cp /backup/source/gitlab.rb /opt/docker-data/gitlab/config/

# [!] consider restoring /etc/gitlab/ssh_host_*_key* files

# Stop the processes that are connected to the database
docker exec -it gitlab gitlab-ctl stop puma
docker exec -it gitlab gitlab-ctl stop sidekiq

# Verify that the processes are all down before continuing
docker exec -it gitlab gitlab-ctl status

# Run the restore. NOTE: "_gitlab_backup.tar" is omitted from the name
docker exec -it gitlab gitlab-backup restore BACKUP=1668535228_2022_11_15_14.8.2

# Restart the GitLab container
docker restart gitlab

until [ "`docker inspect -f {{.State.Health.Status}} gitlab`" == "healthy" ]; do echo "Waiting for container..."; sleep 2; done;
docker inspect -f {{.State.Health.Status}} gitlab

# Check GitLab
docker exec -it gitlab gitlab-rake gitlab:check SANITIZE=true
```
(optional) Do some [checks](https://docs.gitlab.com/ee/update/plan_your_upgrade.html#pre-upgrade-and-post-upgrade-checks)

### Database
* https://docs.gitlab.com/omnibus/settings/database.html
* https://docs.gitlab.com/ee/development/database/db_dump.html
* https://docs.gitlab.com/ee/administration/postgresql/moving.html


Re-seed the database. Usually this is not needed: `gitlab-ctl reconfigure` takes care of this. May be necessary
during tests if DB config on Gitlab's side has not been changed, but the database itself was deleted.
```shell
# https://docs.gitlab.com/omnibus/settings/database.html#seed-the-database-fresh-installs-only

# Stop all the processes that are connected to the database
gitlab-ctl stop  gitlab-exporter
gitlab-ctl stop puma
gitlab-ctl stop sidekiq

# A fix for the script not being able to re-create the DB
# ALTER USER gitlab CREATEDB;
# Remove CREATEDB permission again
# ALTER USER gitlab NOCREATEDB;
# View connections on 'database "gitlabhq_production" is being accessed by other users' error
# SELECT pid, datname, usename, application_name, client_hostname, client_port, backend_start, state FROM pg_stat_activity where datname = 'gitlabhq_production';

# force=yes disables "You will lose any previous data stored in the database.
# Do you want to continue (yes/no)?" prompt
DISABLE_DATABASE_ENVIRONMENT_CHECK=1 gitlab-rake gitlab:setup force=yes
gitlab-ctl start  gitlab-exporter
gitlab-ctl start puma
gitlab-ctl start sidekiq

# View logs
gitlab-ctl tail
```

```shell
# Postgres shipped with the linux package
# View version
/opt/gitlab/embedded/bin/pg_dump --version
/opt/gitlab/embedded/bin/psql --version
# DB location
ls -lha /var/opt/gitlab/postgresql/

# /opt/gitlab/bin/gitlab-psql is a wrapper script that runs psql as user gitlab-psql and
# connects to gitlabhq_production in /var/opt/gitlab/postgresql/ 
sudo gitlab-psql
# Same as gitlab-psql script
sudo su -s /bin/bash - gitlab-psql
psql -h /var/opt/gitlab/postgresql/ gitlabhq_production
# Dump DB to a remote host
# -F, --format=c|d|t|p   output file format (custom, directory, tar, plain text (default))
read -s -p "Password: " my_pwd; echo ""; export my_pwd
pg_dump -h /var/opt/gitlab/postgresql/ gitlabhq_production -Fc | PGPASSWORD="$my_pwd" pg_restore -h remote-host.domain.tld -U postgres -d gitlabhq_production

gitlab-ctl pg-upgrade -V 14
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

### CI/CD

* https://www.digitalocean.com/community/tutorials/how-to-set-up-a-continuous-deployment-pipeline-with-gitlab-ci-cd-on-ubuntu-18-04


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
