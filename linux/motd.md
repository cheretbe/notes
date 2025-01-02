* https://raymii.org/s/tutorials/Disable_dynamic_motd_and_motd_news_spam_on_Ubuntu_18.04.html
* https://linuxsheet.com/answers/1453749u/

```shell
# This is a Python script
/etc/update-motd.d/99-ansible-custom
```

```shell
# Remove unnecessary motd text on Ubuntu
chmod -x /etc/update-motd.d/10-help-text
# /var/lib/ubuntu-advantage/hide-esm-in-motd is older location and is deprecated
# touch /var/lib/ubuntu-advantage/hide-esm-in-motd
touch /var/lib/update-notifier/hide-esm-in-motd
rm -rf /var/lib/update-notifier/updates-available
apt update
```
