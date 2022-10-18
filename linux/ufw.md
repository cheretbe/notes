* https://help.ubuntu.com/community/UFW
* https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-22-04

```shell
# [!!] Double check before doing anything else when setting up via ssh
sudo ufw status verbose

sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
# if SSH server runs on a different port
sudo ufw allow 2222

sudo ufw enable

sudo ufw status numbered
sudo ufw delete 2
```
