* http://backuppc.sourceforge.net/
* https://github.com/backuppc/backuppc
* https://github.com/backuppc/backuppc/wiki/Installing-BackupPC-4-from-tarball-or-git-on-Ubuntu

### Installation
Only for new installation, skip this for upgrade
```shell
apt-get install apache2 apache2-utils libapache2-mod-perl2 smbclient sendmail libapache2-mod-scgi \
    libarchive-zip-perl libfile-listing-perl libxml-rss-perl libcgi-session-perl

adduser --system --home /var/lib/backuppc --group --disabled-password --shell /bin/false backuppc

rmdir /var/lib/backuppc/
mkdir /path/to/backup/dir
chown backuppc:backuppc /path/to/backup/dir
ln -s /path/to/backup/dir /var/lib/backuppc

mkdir -p /var/lib/backuppc/.ssh
chmod 700 /var/lib/backuppc/.ssh
# [!] 'StrictHostKeyChecking no' parameter is optional, it allows connecting to any host
# without explicityly adding it to .ssh/known_hosts
echo -e "BatchMode yes\nStrictHostKeyChecking no" > /var/lib/backuppc/.ssh/config
ssh-keygen -q -t rsa -b 4096 -N '' -C "BackupPC key" -f /var/lib/backuppc/.ssh/id_rsa
chmod 600 /var/lib/backuppc/.ssh/id_rsa
chmod 644 /var/lib/backuppc/.ssh/id_rsa.pub
chown -R backuppc:backuppc /var/lib/backuppc/.ssh
```

Check and download the lastest released versions:
* https://github.com/backuppc/backuppc-xs/releases/
* https://github.com/backuppc/rsync-bpc/releases/
* https://github.com/backuppc/rsync-bpc/releases/
```shell
mkdir -p sources
cd sources
wget https://github.com/backuppc/backuppc-xs/releases/download/0.57/BackupPC-XS-0.57.tar.gz
wget https://github.com/backuppc/rsync-bpc/releases/download/3.0.9.12/rsync-bpc-3.0.9.12.tar.gz
wget https://github.com/backuppc/backuppc/releases/download/4.2.1/BackupPC-4.2.1.tar.gz
tar -xzvf BackupPC-XS-0.57.tar.gz
tar -xzvf rsync-bpc-3.0.9.12.tar.gz
tar -xzvf BackupPC-4.2.1.tar.gz
```
Install dependencies
```shell
cd BackupPC-XS-0.57/
perl Makefile.PL
make
make test
make install

cd ../rsync-bpc-3.0.9.12/
./configure
make
make install
```
Install BackupPC
```shell
cd ../BackupPC-4.2.1/
# [!] When installing, use this
# ./configure.pl --batch --cgi-dir /var/www/cgi-bin/BackupPC --data-dir /var/lib/backuppc \
#   --hostname backuppc --html-dir /var/www/html/BackupPC --html-dir-url /BackupPC \
#   --install-dir /usr/local/BackupPC

# When upgrading, use this instead:
./configure.pl --batch --config-path /etc/BackupPC/config.pl
```
