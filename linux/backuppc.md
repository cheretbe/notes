* http://backuppc.sourceforge.net/
* https://github.com/backuppc/backuppc
* https://github.com/backuppc/backuppc/wiki/Installing-BackupPC-4-from-tarball-or-git-on-Ubuntu

### Installation

```shell
apt-get install apache2 apache2-utils libapache2-mod-perl2 smbclient sendmail libapache2-mod-scgi \
    libarchive-zip-perl libfile-listing-perl libxml-rss-perl libcgi-session-perl
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
