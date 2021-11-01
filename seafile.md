```shell
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
* https://git.fws.fr/fws/ansible-roles/src/branch/master/roles/seafile

### Server
* Logs are in `/opt/seafile/logs/`
* https://shoeper.gitbooks.io/seafile-docs/content/deploy/using_logrotate.html
* https://shoeper.gitbooks.io/seafile-docs/content/security/fail2ban.html

### seaf-cli
```shell
sudo wget https://linux-clients.seafile.com/seafile.asc -O /usr/share/keyrings/seafile-keyring.asc
# Ubuntu 20.04
sudo bash -c "echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/seafile-keyring.asc] https://linux-clients.seafile.com/seadrive-deb/focal/ stable main' > /etc/apt/sources.list.d/seadrive.list"
apt update
apt install seafile-cli

mkdir ~/seafile-client 
# ~/.ccnet directory must not exist at this point
seaf-cli init -d ~/seafile-client
seaf-cli start

# Find out library IDs
seaf-cli list-remote -s http://seafile-test -u admin@seafile.local
seaf-cli sync -l 00000000-0000-0000-0000-000000000000 -s http://seafile-test -d ~/Documents/library_name -u admin@seafile.local
```
