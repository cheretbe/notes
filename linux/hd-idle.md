Download source: https://sourceforge.net/projects/hd-idle/

```shell
apt install debhelper

# Add -uc -us options on gpg error
# gpg: skipped "Christian Mueller <cm1@mumac.de>": secret key not available
# gpg: dpkg-sign.w89DF9ru/hd-idle_1.04.dsc: clearsign failed: secret key not available
dpkg-buildpackage -rfakeroot
dpkg -i ../hd-idle_*.deb
```
