* https://github.com/haiwen/seafile
* https://github.com/haiwen/seafile-server-installer
* https://manual.seafile.com/deploy_pro/real_time_backup/
* https://github.com/search?q=filename%3A*.service+seaf-cli
    * https://help.seafile.com/syncing_client/linux-cli/
    * https://gist.github.com/drmalex07/d006f12914b21198ee43
    * https://www.freedesktop.org/software/systemd/man/systemd.service.html


### seaf-cli
```shell
sudo wget https://linux-clients.seafile.com/seafile.asc -O /usr/share/keyrings/seafile-keyring.asc
# Ubuntu 20.04
sudo bash -c "echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/seafile-keyring.asc] https://linux-clients.seafile.com/seadrive-deb/focal/ stable main' > /etc/apt/sources.list.d/seadrive.list"
apt update
apt install seadrive-cli
```
