* :warning::warning: Syncing with existing directory gothcha:
    * first select **parent** directory **without clicking** on *sync with an existing folder*
    * then click on *sync with an existing folder* and make sure target subdirectory was added to the path
    * click OK and **double check** what's being downloaded


Auto-start client on Linux: run `Startup Applications preferences`, add item `seafile-applet` (`Seafile desktop sync client`)


```shell
/opt/seafile/seafile-server-latest/seaf-gc.sh --dry-run

# https://www.seafile.com/api/client-updates/seafile-client-windows/appcast.xml
curl -s https://www.seafile.com/api/client-updates/seafile-client-windows/appcast.xml | xmlstarlet select --template -v '/rss/channel/item/enclosure/@url' -nl
```
```python
import xml.etree.ElementTree
xmlData = xml.etree.ElementTree.parse("appcast.xml")
xmlData.find('//channel/item/enclosure').attrib["url"]
```

* Before version 6.0, the source code of "sync client daemon" and "server core" was mixed together in https://github.com/haiwen/seafile. But after 6.0 version, the server core is separated into its own repository. For this reason, the sync client daemon repository is still the "front page" for Seafile project on Github.
    * Sync client daemon (this repository): https://github.com/haiwen/seafile
    * Sync client GUI: https://github.com/haiwen/seafile-client
        * https://github.com/haiwen/seafile/blob/master/app/seaf-cli
    * Server core: https://github.com/haiwen/seafile-server
    * Server web UI: https://github.com/haiwen/seahub
    * iOS app: https://github.com/haiwen/seafile-iOS
    * Android app: https://github.com/haiwen/seadroid
    * WebDAV: https://github.com/haiwen/seafdav
* https://github.com/haiwen/seafile-server-installer
* https://manual.seafile.com/deploy_pro/real_time_backup/
* https://github.com/search?q=filename%3A*.service+seaf-cli
    * :point_right: https://shoeper.gitbooks.io/seafile-docs/content/deploy/start_seafile_at_system_bootup.html
    * https://help.seafile.com/syncing_client/linux-cli/
    * https://gist.github.com/drmalex07/d006f12914b21198ee43
    * https://www.freedesktop.org/software/systemd/man/systemd.service.html
* :point_right: https://git.fws.fr/fws/ansible-roles/src/branch/master/roles/seafile

### Server
* Logs are in `/opt/seafile/logs/`
* https://shoeper.gitbooks.io/seafile-docs/content/deploy/using_logrotate.html
* :warning: fail2ban
    * https://shoeper.gitbooks.io/seafile-docs/content/security/fail2ban.html
    * https://manual.seafile.com/security/fail2ban/
* `/opt/seafile/conf/seafile.conf`
    * :warning: restart after editing options: `systemctl restart seafile-server`
    * https://manual.seafile.com/config/seafile-conf/
    * https://manual.seafile.com/config/seafile-conf/#seafile-fileserver-configuration
    * New in Seafile Pro 7.1.16 and Pro 8.0.3: You can set the maximum number of files contained in a library that can be synced by the Seafile client. The default is 100000. When you download a repo, Seafile client will request fs id list, and you can control the timeout period of this request through fs_id_list_request_timeout configuration, which defaults to 5 minutes. These two options are added to prevent long fs-id-list requests from overloading the server. Since Pro 8.0.4 version, you can **set both options to -1**, to allow unlimited size and timeout.
    ```
    [fileserver]
    max_sync_file_count = -1
    fs_id_list_request_timeout = -1
    ```
    * https://forum.seafile.com/t/size-too-large-changes-in-ccnet-and-seafile-conf-without-effect/15025
    * Fix for `Size too large` error
    ```
    [fileserver]
    # Set maximum upload file size to 200M.
    # If not configured, there is no file size limit for uploading.
    max_upload_size=200
    # Set maximum download directory size to 200M.
    # Default is 100M.
    max_download_dir_size=200
    ```
* Advanced settings are in `/opt/seafile/conf/seahub_settings.py` (some of them can be changed in admin settings dialog) - https://manual.seafile.com/config/seahub_settings_py/
    ```python
    # Max number of files when user upload file/folder.
    # Since version 6.0.4
    MAX_NUMBER_OF_FILES_FOR_FILEUPLOAD = 500
    ```

### Installation
* Docker
* https://github.com/haiwen/seafile-server-installer/blob/master/seafile-9.0_ubuntu
  * Creates `/opt/seafile/aio_seafile-server.log`, that contains admin password (mode is `0600` though)

#### Docker

* https://github.com/cheretbe/docker-configs/tree/main/seafile
    * :point_right: https://github.com/cheretbe/docker-configs/blob/main/seafile/README.md#version-upgrade
* https://manual.seafile.com/docker/pro-edition/deploy_seafile_pro_with_docker/
    * https://manual.seafile.com/docker/pro-edition/docker-compose.yml
* https://manual.seafile.com/docker/cluster/deploy_seafile_cluster_with_docker/
* https://manual.seafile.com/docker/upgrade/upgrade_docker/
* https://itsfoss.com/deploy-seafile-server-docker/
* Source code: https://github.com/haiwen/seafile-docker

##### Non-Docker to Docker migration

* https://manual.seafile.com/docker/non_docker_to_docker/

```shell
# cd /opt/seafile/seafile-server-latest/
# ./seafile.sh stop  && ./seahub.sh stop
service seafile-server stop
update-rc.d seafile-server disable

systemctl stop nginx &&  systemctl disable nginx
systemctl stop memcached &&  systemctl disable memcached

# The original guide proposes modifying original DB and granting seafile
# user access from any IP. But since we are going to use a container for DB,
# we will do this in the container itself, leaving the original intact
systemctl stop mariadb.service && systemctl disable mariadb.service

# /opt/seafile-data         -> /opt/docker-data/seafile/data
# /opt/seafile-data/seafile    /opt/docker-data/seafile/data/seafile

mkdir -p /opt/docker-data/seafile/data/seafile
mkdir    /opt/docker-data/seafile/data/seafile/ccnet

cp -r /opt/seafile/conf  /opt/docker-data/seafile/data/seafile
cp -r /opt/seafile/seahub-data  /opt/docker-data/seafile/data/seafile

cd /opt/docker-data/seafile/data/seafile/conf/

# Update ccnet.conf, seafile.conf, seafevents.conf, seahub_settings.py
# change HOST=127.0.0.1 to HOST=db
#
# Update seahub_settings.py
# 'LOCATION': 'memcached:11211'

mariadb --version
# 10.3.34
# MARIADB_IMAGE_VERSION=10.3.34

cp -r /opt/seafile/seafile-data /opt/docker-data/seafile/data/seafile/

mkdir -p /opt/docker-data/seafile/mysql/db/
cp -r /var/lib/mysql/* /opt/docker-data/seafile/mysql/db/

# [!] Just db container is being started
docker compose up db -d

cat /root/.my.cnf
docker exec -it seafile-mysql mysql -p
```
```sql
## Change the password according to the actual password you use
## cat /opt/docker-data/seafile/data/seafile/conf/ccnet.conf
GRANT ALL PRIVILEGES ON *.* TO 'seafile'@'%' IDENTIFIED BY 'your-password' WITH GRANT OPTION;

## Grant seafile user can connect the database from any IP address
GRANT ALL PRIVILEGES ON `ccnet_db`.* to 'seafile'@'%';
GRANT ALL PRIVILEGES ON `seafile_db`.* to 'seafile'@'%';
GRANT ALL PRIVILEGES ON `seahub_db`.* to 'seafile'@'%';
```

```shell
docker compose restart db
docker compose up -d
```


#### Elasticsearch config
* https://manual.seafile.com/deploy_pro/details_about_file_search/
    * Settings are in `/opt/seafile/conf/seafevents.conf` (`[INDEX FILES]` section) 
* Out of memory error fix
    * https://forums.docker.com/t/elastic-search-container-out-of-memory/43148/2
    * https://github.com/elastic/elasticsearch-docker/issues/43#issuecomment-343997733
    ```shell
    docker exec -it seafile-elasticsearch bash
    # heap_used_percent, heap_max_in_bytes
    curl --fail --silent --show-error localhost:9200/_nodes/stats | jq '.nodes[].jvm.mem'
    ```

### Maintenance

* https://manual.seafile.com/maintain/
* Garbage collection 
    * :point_right: use `screen` 
    * :warning: Garbage collector takes in account libraries' history settings (will not delete anything if it is set to "keep full history")
    ```shell
    du -hs /shared/seafile/seafile-data/
    du -hs /opt/seafile
    sudo du -sh /opt/docker-data/seafile/data/
    
    /opt/seafile/seafile-server-latest/seaf-gc.sh --dry-run
    # Docker (/scripts/gc.sh is a wrapper around seaf-gc.sh that stops the service for CE)
    docker exec seafile /scripts/gc.sh --dry-run
    
    /opt/seafile/seafile-server-latest/seaf-gc.sh --dry-run
    ```
* FSCK
    ```shell
    # https://manual.seafile.com/maintain/seafile_fsck/
    # "--shallow" or "-s" doesn't calculate hashes for files contents (speeds up checks greatly)
    # "--export" allows to copy all files from a library without relying on server's database
    # Readonly fsck
    docker exec seafile /opt/seafile/seafile-server-latest/seaf-fsck.sh
    ```
* DB cleanup
    * https://manual.seafile.com/maintain/clean_database/
    ```shell
    # [!!] for migrated Docker instance the password in the password manager
    # Root password is in MYSQL_ROOT_PASSWORD variable
    docker inspect -f '{{ .Config.Env }}' seafile-mysql
    docker exec -it seafile-mysql mysql -p
    ```
-------
* Server-side automation with Python
    * https://github.com/goaxe/lab/blob/master/tools/test_server.py
    * `seafile_api.get_repo_list(-1, -1)` ???
    * https://github.com/haiwen/seafile-server/blob/master/python/seaserv/service.py


### Real time backup
* https://manual.seafile.com/deploy_pro/real_time_backup/
* https://shoeper.gitbooks.io/seafile-docs/content/deploy_pro/real_time_backup.html

:warning: Doesn't work at the moment.
* MySQL replication works
* `/opt/seafile/seafile-server-latest/seaf-backup-cmd.sh sync 00000000-0000-0000-0000-000000000000` fails with error "Failed to sync repo 00000000-0000-0000-0000-000000000000: Failed to get repo info from primary."
* `curl -v https://master.domain.tld/seafhttp/server-sync/repo-list` returns error 400
* https://forum.seafile.com/t/seafile-real-time-backup-server/7090 has a comment "Using real-time backup requires that you have setup the primary server with Nginx or Apache". We did use nginx, but not sure if it served `seafhttp/server-sync/repo-list` correctly. :warning: this needs additional research.

```shell
# Stop Seafile service, so that no update will be written into database
docker compose stop seafile

# on host, container doesn't have editors
sudo nano /opt/docker-data/seafile/mysql/conf/replication.cnf
```
```
[mysqld]
log_bin=mysql-bin
server-id=1
```
```shell
docker compose restart db
docker exec -it seafile-mysql mysql -p
```
```sql
CREATE USER 'repl'@'%' IDENTIFIED BY 'slavepass';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';

FLUSH TABLES WITH READ LOCK;
SHOW MASTER STATUS;
-- Whe need the File and Position fields
```
:warning: Monitor `/opt/docker-data/seafile/mysql/db/mysql-bin.*` size and decide on `expire_logs_days` setting

```shell
mysqldump -u root -p --databases \
  --ignore-table=seafile_db.Repo --ignore-table=seafile_db.Branch --ignore-table=seafile_db.RepoHead \
  --ignore-table=seahub_db.base_userlastlogin --ignore-table=seahub_db.django_session \
  --ignore-table=seahub_db.sysadmin_extra_userloginlog --ignore-table=seahub_db.UserTrafficStat \
  --ignore-table=seahub_db.FileAudit --ignore-table=seahub_db.FileUpdate --ignore-table=seahub_db.PermAudit \
  --ignore-table=seahub_db.Event --ignore-table=seahub_db.UserEvent --ignore-table=seahub_db.avatar_avatar \
  --ignore-table=seahub_db.avatar_groupavatar --ignore-table=seahub_db.avatar_uploaded \
  --master-data seafile_db ccnet_db seahub_db > dbdump.sql
```
####  Backup Server
```
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d

docker-compose.local.yml

services:
  db:
    ports:
      - "3306:3306"


docker run -it --rm mariadb:10.9.3 --verbose --help

sudo nano /opt/docker-data/seafile/mysql/conf/replication.cnf

[mysqld]
server-id=2
replicate-ignore-table = seafile_db.Repo
replicate-ignore-table = seafile_db.Branch
replicate-ignore-table = seafile_db.RepoHead
replicate-ignore-table = seahub_db.base_userlastlogin
replicate-ignore-table = seahub_db.django_session
replicate-ignore-table = seahub_db.sysadmin_extra_userloginlog
replicate-ignore-table = seahub_db.UserTrafficStat
replicate-ignore-table = seahub_db.FileAudit
replicate-ignore-table = seahub_db.FileUpdate
replicate-ignore-table = seahub_db.PermAudit
replicate-ignore-table = seahub_db.avatar_avatar
replicate-ignore-table = seahub_db.avatar_groupavatar
replicate-ignore-table = seahub_db.avatar_uploaded
replicate-ignore-table = seahub_db.Event
replicate-ignore-table = seahub_db.UserEvent

docker-compose.temp-slave.yml

services:
  db:
    command: ["--skip-slave-start"]

docker compose -f docker-compose.yml -f docker-compose.temp-slave.yml up db --force-recreate --build -d

docker inspect -f "{{.Config.Cmd}}" seafile-mysql

# We can create dump file directly on backup 
docker exec -it seafile-mysql bash

mysqldump -h host.domain.tld -u root -p --databases \
  --ignore-table=seafile_db.Repo --ignore-table=seafile_db.Branch --ignore-table=seafile_db.RepoHead \
  --ignore-table=seahub_db.base_userlastlogin --ignore-table=seahub_db.django_session \
  --ignore-table=seahub_db.sysadmin_extra_userloginlog --ignore-table=seahub_db.UserTrafficStat \
  --ignore-table=seahub_db.FileAudit --ignore-table=seahub_db.FileUpdate --ignore-table=seahub_db.PermAudit \
  --ignore-table=seahub_db.Event --ignore-table=seahub_db.UserEvent --ignore-table=seahub_db.avatar_avatar \
  --ignore-table=seahub_db.avatar_groupavatar --ignore-table=seahub_db.avatar_uploaded \
  --master-data seafile_db ccnet_db seahub_db > dbdump.sql
  
mysql -u root -p < dbdump.sql

mysql -h host.domain.tld -u root -p -Be "unlock tables;"

CHANGE MASTER TO MASTER_HOST='host.domain.tld', MASTER_USER='repl', MASTER_PASSWORD='slavepass', MASTER_LOG_FILE='bin-log-file', MASTER_LOG_POS=position;
```

### WebDAV

* (seems like installation script is more up-to-date) https://manual.seafile.com/extension/webdav/
* Client config: [./linux/dafvs2.md](./linux/dafvs2.md) (:warning: Everything is already there, including auto-mounting, just look closely :wink:)

### seaf-cli
```shell
sudo wget https://linux-clients.seafile.com/seafile.asc -O /usr/share/keyrings/seafile-keyring.asc
# Ubuntu 18.04+
sudo bash -c "echo 'deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/seafile-keyring.asc] https://linux-clients.seafile.com/seafile-deb/$(lsb_release -cs)/ stable main' > /etc/apt/sources.list.d/seafile.list"
apt update
apt-cache policy seafile-cli
apt install seafile-cli
# binary is /usr/bin/seaf-cli

# From the docs: init - This command initializes the config dir. It also creates sub-directories "seafile-data" and "seafile"
# under parent-dir. "seafile-data" is used to store internal data, while "seafile" is used as the default location put downloaded libraries.
# Actually "seafile" is not used by default (-d parameter is required for sync command)
mkdir ~/seafile-client 
# ~/.ccnet directory must not exist at this point (data directory must exist, see mkdir above)
seaf-cli init -d ~/seafile-client
# No default server config, everything is done per library with sync command
seaf-cli start

# Find out library IDs
seaf-cli list-remote -s http://seafile-test -u admin@seafile.local
# -d (local dir) must exist
seaf-cli sync -l 00000000-0000-0000-0000-000000000000 -s http://seafile-test -d ~/Documents/library_name -u admin@seafile.local
```
* Systemd unit example
    * https://manual.seafile.com/deploy/start_seafile_at_system_bootup/#create-systemd-service-file-etcsystemdsystemseafile-clientservice-optional

### Nginx reverse proxy

```
server {
    listen 80;
    server_name _ default_server;

    # (optional) allow certbot to connect to challenge location via HTTP Port 80
    # location /.well-known/acme-challenge/ {
    #     alias /var/www/challenges/;
    #     try_files $uri =404;
    # }

    location / {
        rewrite ^ https://$host$request_uri? permanent;
    }
}

server {
    server_name  seafile.domain.tld;
    listen       443 ssl http2;

    ssl_certificate ssl/seafile.domain.tld.bundle.crt;
    ssl_certificate_key ssl/seafile.domain.tld.key;

    ssl_protocols TLSv1.2 TLSv1.1 TLSv1;
    ssl_prefer_server_ciphers on;
    ssl_ciphers EECDH+ECDSA+AESGCM:EECDH+aRSA+AESGCM:EECDH+ECDSA+SHA512:EECDH+ECDSA+SHA384:EECDH+ECDSA+SHA256:ECDH+AESGCM:ECDH+AES256:DH+AESGCM:DH+AES256:RSA+AESGCM:!aNULL:!eNULL:!LOW:!RC4:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS;

    ssl_session_cache shared:TLS:2m;

    location / {
        proxy_pass         http://127.0.0.1:8080;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;

        proxy_set_header   X-Forwarded-Proto $scheme;
        #proxy_set_header   X-Forwarded-Proto http;

        client_max_body_size 0;
        proxy_connect_timeout  36000s;
        proxy_read_timeout  36000s;
        proxy_send_timeout  36000s;
        send_timeout  36000s;
        proxy_request_buffering off;
    }
}
```
