* https://github.com/jimsalterjrs/sanoid/issues/116#issuecomment-318468961

```shell
# Installation
# ------------
# Ubuntu
apt install libconfig-inifiles-perl pv lzop mbuffer libcapture-tiny-perl jq
# CentOS
yum install perl-Config-IniFiles perl-Data-Dumper mbuffer lzop pv

cd /opt/
wget https://github.com/jimsalterjrs/sanoid/archive/$(curl -s https://api.github.com/repos/jimsalterjrs/sanoid/releases/latest | jq -r ".tag_name").tar.gz

tar xzvf v2.2.0.tar.gz
ln -s sanoid-2.2.0/ sanoid

# Copy sample configs
mkdir -p /etc/sanoid
cp /opt/sanoid/sanoid.defaults.conf /etc/sanoid/
cp /opt/sanoid/sanoid.conf /etc/sanoid/

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

Hourly `/etc/cron.d/sanoid` example
```
# Run Sanoid every hour
05 * * * * root /opt/sanoid/sanoid --cron
```

### Syncoid

```shell
/opt/sanoid/syncoid pool/path syncoid-backup@host.tld:pool/path --recursive --sshkey /path/to/syncoid-backup.key
```

:warning: Syncoid's `--no-privilege-elevation` option would have worked, but linux can't mount newly created datasets
```shell
# 
zfs allow -u syncoid-backup-user compression,mountpoint,create,mount,receive,destroy pool/path
```
* https://github.com/jimsalterjrs/sanoid/pull/140
* https://github.com/zfsonlinux/zfs/pull/4487
* https://askubuntu.com/questions/843585/how-to-let-non-root-user-take-zfs-snapshot
* https://dan.langille.org/2015/02/16/zfs-send-zfs-receive-as-non-root/

`/etc/sudoers.d/syncoid` as a workaround
```
# Allow ZFS operations during sync
syncoid-backup ALL=(ALL) NOPASSWD: /sbin/zfs
```

```shell
# on client
apt install lzop mbuffer
```

Daily backup script example
```
# Backup daily at 15:00
00 15  *  *  *    root /path/to/offsite_backup.sh >>/path/to/offsite_backup.log 2>&1
```
:warning: Change `/path/to/offsite_backup.log` to actual log file path
```shell
# Log rotation
cat >/etc/logrotate.d/zfs-offsite-backup <<EOL
/path/to/offsite_backup.log {
  monthly
  rotate 3
  size 50M
  compress
  delaycompress
  missingok
  notifempty
}
EOL

# Don't allow group writing to the file in order to avoid logrotate skipping rotation
chmod 644 /etc/logrotate.d/zfs-offsite-backup
# Check log rotation status
logrotate -d /etc/logrotate.d/zfs-offsite-backup
```

```bash
#!/bin/bash

status_file_path="/path/to/offsite_backup_status"

echo "-----------------------------------------------"
echo "$(date -Iseconds) Starting backup"

echo "$(date -Iseconds) Creating snapshots"
/opt/sanoid/sanoid --cron
if [ $? -ne 0 ]; then
  echo "$(date -Iseconds) Sanoid call has failed"
  echo "$(date -Iseconds);CRITICAL;Sanoid call has failed" >${status_file_path}
  exit 1
fi

echo "$(date -Iseconds) Replicating to remote filesystem"
/opt/sanoid/syncoid pool/path user@host.tld:pool/path --recursive --sshkey /path/to/a/key
if [ $? -ne 0 ]; then
  echo "$(date -Iseconds) Syncoid call has failed"
  echo "$(date -Iseconds);CRITICAL;Syncoid call has failed" >${status_file_path}
  exit 1
fi

echo "$(date -Iseconds) Offsite backup was successful"
echo "$(date -Iseconds);OK;Offsite backup was successful" >${status_file_path}
exit 0
```
