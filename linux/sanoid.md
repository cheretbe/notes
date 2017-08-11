* https://github.com/jimsalterjrs/sanoid/issues/116#issuecomment-318468961

```shell
# Ubunut
apt install libconfig-inifiles-perl pv lzop mbuffer
# CentOS
yum install perl-Config-IniFiles perl-Data-Dumper mbuffer lzop pv

mkdir -p /etc/sanoid
cp sanoid-1.4.14/sanoid.defaults.conf /etc/sanoid/
cp sanoid-1.4.14/sanoid.conf /etc/sanoid/
```
