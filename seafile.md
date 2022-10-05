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
* https://shoeper.gitbooks.io/seafile-docs/content/security/fail2ban.html
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
* Maintenance
    * https://manual.seafile.com/maintain/
    * `/opt/seafile/seafile-server-latest/seaf-gc.sh --dry-run` 

### Real time backup
* https://manual.seafile.com/deploy_pro/real_time_backup/
* https://shoeper.gitbooks.io/seafile-docs/content/deploy_pro/real_time_backup.html

### Installation
* :warning: https://manual.seafile.com/docker/non_docker_to_docker/
* https://github.com/haiwen/seafile-server-installer/blob/master/seafile-9.0_ubuntu
  * Creates `/opt/seafile/aio_seafile-server.log`, that contains admin password (mode is `0600` though)
  * 

### WebDAV

* (seems like installation script is more up-to-date) https://manual.seafile.com/extension/webdav/
* Client config: [./linux/dafvs2.md](./linux/dafvs2.md) (:warning: Everything is already there, including auto-mounting, just look closely :wink:)

### seaf-cli
```shell
sudo wget https://linux-clients.seafile.com/seafile.asc -O /usr/share/keyrings/seafile-keyring.asc
# Ubuntu 20.04
sudo bash -c "echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/seafile-keyring.asc] https://linux-clients.seafile.com/seadrive-deb/focal/ stable main' > /etc/apt/sources.list.d/seadrive.list"
apt update
apt install seafile-cli
# binary is /usr/bin/seaf-cli

mkdir ~/seafile-client 
# ~/.ccnet directory must not exist at this point
seaf-cli init -d ~/seafile-client
seaf-cli start

# Find out library IDs
seaf-cli list-remote -s http://seafile-test -u admin@seafile.local
seaf-cli sync -l 00000000-0000-0000-0000-000000000000 -s http://seafile-test -d ~/Documents/library_name -u admin@seafile.local
```
