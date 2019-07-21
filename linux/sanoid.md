* https://github.com/jimsalterjrs/sanoid/issues/116#issuecomment-318468961

```shell
# Ubuntu
apt install libconfig-inifiles-perl pv lzop mbuffer
# CentOS
yum install perl-Config-IniFiles perl-Data-Dumper mbuffer lzop pv

# Copy sample configs
mkdir -p /etc/sanoid
cp sanoid-1.4.14/sanoid.defaults.conf /etc/sanoid/
cp sanoid-1.4.14/sanoid.conf /etc/sanoid/

# Nagios monitoring
/opt/sanoid/sanoid --monitor-health
/opt/sanoid/sanoid --monitor-snapshots
```

`/etc/sanoid/sanoid.conf` example:
```
[pool/path]
        use_template = backup
        recursive = yes

#############################
# templates below this line #
#############################

[template_backup]
        hourly = 0
        daily = 30
        monthly = 3
        yearly = 0
        autosnap = yes
        autoprune = yes

        hourly_warn = 0
        hourly_crit = 0
```
