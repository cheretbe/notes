* http://backuppc.sourceforge.net/
* https://github.com/backuppc/backuppc
* https://sourceforge.net/p/backuppc/mailman/
* https://github.com/backuppc/backuppc/wiki/Installing-BackupPC-4-from-tarball-or-git-on-Ubuntu
* https://serverfault.com/questions/662027/backuppc-schedule-advanced-settings/662150#662150
* https://gogs.zionetrix.net/bn8/check_backuppc
* Review:
    * https://sourceforge.net/p/backuppc/mailman/message/33596562/
    * http://www.guyrutenberg.com/2014/01/14/restricting-ssh-access-to-rsync/


:warning: For SMB and tar, BackupPC uses the modification time (mtime) to determine which files have changed since the last backup. That means SMB and tar incrementals **are not able to detect** deleted files, renamed files or new files whose modification time is prior to the last lower-level backup.
* https://backuppc.github.io/backuppc/BackupPC.html#Backup-basics

```shell
# View zlib-compressed log file
printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" | cat - XferLOG.5.z | gzip -dc | less
# or use BackupPC_zcat - as backuppc user (!)
/usr/local/BackupPC/bin/BackupPC_zcat /var/lib/backuppc/pc/hostname/XferLOG.1.z

# List backup contents
/usr/local/BackupPC/bin/BackupPC_ls -h hostname -n 26 -s /home /
```

### Config

[$Conf{FullKeepCnt}](https://backuppc.github.io/backuppc/BackupPC.html#_conf_fullkeepcnt_): `1*$Conf{FillCycle}, 2*$Conf{FillCycle}, 4*$Conf{FillCycle}, 8*$Conf{FillCycle}, etc.`<br>
With defaults `$Conf{FillCycle} = 0;` and `$Conf{FullPeriod} = 6.97;` this gives us the following exponential sequence:<br>
`1 week, 2 weeks, 1 month, 2 months, 4 months, 8 months, etc.`
```perl
$Conf{FullKeepCnt} = [
  4,
  6,
  12,
  12,
  5
];
$Conf{FullAgeMax} = 1240;
$Conf{IncrKeepCnt} = 30;
$Conf{IncrAgeMax} = 60;
```

:warning: Don't copy/paste this code directly, use [edit_as_utf8.py](https://github.com/cheretbe/backuppc-scripts/blob/master/util/edit_as_utf8.py) script<br>
:warning: Note double qoutes on non-iso-8859-1 strings
```perl
# Typical Windows exculdes
$Conf{BackupFilesExclude} = {
  '*' => [
    '/pagefile.sys',
    '/swapfile.sys',
    '/hiberfil.sys',
    '/$Recycle.Bin',
    '/RECYCLER',
    '/RECYCLED',
    '/System Volume Information',

    '/Documents and Settings',
    '/Program Files/AVAST Software/Avast',
    '/ProgramData/Application Data',
    '/ProgramData/AVAST Software/Avast',
    '/ProgramData/Desktop',
    '/ProgramData/Documents',
    '/ProgramData/Favorites',
    '/ProgramData/Microsoft/Diagnosis',
    '/ProgramData/Microsoft/Network/Downloader',
    '/ProgramData/Microsoft/RAC',
    '/ProgramData/Microsoft/Windows Defender',
    '/ProgramData/Microsoft/Windows/LocationProvider',
    '/ProgramData/Microsoft/Windows/SystemData',
    '/ProgramData/Microsoft/Windows/WER',
    '/ProgramData/Start Menu',
    '/ProgramData/Templates',
    '/Users/*/AppData/Local/Application Data',
    '/Users/*/AppData/Local/Google/Chrome/User Data/*/Application Cache',
    '/Users/*/AppData/Local/Google/Chrome/User Data/*/Cache',
    '/Users/*/AppData/Local/Google/Chrome/User Data/*/Code Cache',
    '/Users/*/AppData/Local/Google/Chrome/User Data/*/GPUCache',
    '/Users/*/AppData/Local/Google/Chrome/User Data/*/History Provider Cache',
    '/Users/*/AppData/Local/Google/Chrome/User Data/*/IndexedDB',
    '/Users/*/AppData/Local/Google/Chrome/User Data/*/Service Worker/CacheStorage',
    '/Users/*/AppData/Local/Google/Chrome/User Data/*/Service Worker/ScriptCache',
    '/Users/*/AppData/Local/History',
    '/Users/*/AppData/Local/Microsoft/Windows/Explorer/ThumbCacheToDelete',
    '/Users/*/AppData/Local/Microsoft/Windows/INetCache',
    '/Users/*/AppData/Local/Microsoft/Windows/Temporary Internet Files',
    '/Users/*/AppData/Local/Mozilla/Firefox',
    '/Users/*/AppData/Local/Opera Software/Opera Stable/Cache',
    '/Users/*/AppData/Local/Opera/Opera/cache',
    '/Users/*/AppData/Local/Temp',
    '/Users/*/AppData/Local/Temporary Internet Files',
    '/Users/*/AppData/Roaming/Mozilla/Firefox/Crash Reports',
    '/Users/*/AppData/Roaming/XnView/XnView.db',
    '/Users/*/AppData/Roaming/XnViewMP/Thumb.db',
    '/Users/*/Application Data',
    '/Users/*/Cookies',
    '/Users/*/Documents/My Music',
    '/Users/*/Documents/My Pictures',
    '/Users/*/Documents/My Videos',
    '/Users/*/Downloads',
    '/Users/*/Local Settings',
    '/Users/*/My Documents',
    '/Users/*/NetHood',
    '/Users/*/PrintHood',
    '/Users/*/Recent',
    '/Users/*/SendTo',
    '/Users/*/Start Menu',
    '/Users/*/Templates',
    '/Users/All Users',
    '/Users/Default User',
    '/Windows/CSC',
    '/Windows/memory.dmp',
    '/Windows/Minidump',
    '/Windows/netlogon.chg',
    '/Windows/Prefetch',
    '/Windows/Resources/Themes/aero/VSCache',
    '/Windows/SoftwareDistribution',
    '/Windows/System32/Bits.bak',
    '/Windows/System32/Bits.log',
    '/Windows/system32/LogFiles/WMI/RtBackup',
    '/Windows/system32/MSDtc/MSDTC.LOG',
    '/Windows/system32/MSDtc/trace/dtctrace.log',
    '/Windows/Temp',

    "/Program Files/Windows NT/Стандартные",
    "/ProgramData/Microsoft/Windows/Start Menu/Программы",
    "/ProgramData/Главное меню",
    "/ProgramData/Документы",
    "/ProgramData/Избранное",
    "/ProgramData/Рабочий стол",
    "/ProgramData/Шаблоны",
    "/Users/*/AppData/Roaming/Microsoft/Windows/Start Menu/Программы",
    "/Users/*/Documents/Мои видеозаписи",
    "/Users/*/Documents/Мои рисунки",
    "/Users/*/Documents/Моя музыка",
    "/Users/*/Главное меню",
    "/Users/*/Мои документы",
    "/Users/*/Шаблоны",
    "/Users/Все пользователи",

    'Users/*/AppData/Local/SpiderOak',
    '/temp/!_no_backup',
    '/temp/_no_backup'
  ]
};
```

### Installation
Only for new installation, skip this for upgrade
```shell
apt-get install apache2 apache2-utils libapache2-mod-perl2 smbclient rrdtool libapache2-mod-scgi \
    libarchive-zip-perl libfile-listing-perl libxml-rss-perl libcgi-session-perl make gcc par2 \
    libacl1 libacl1-dev
    
# Check if sendmail is installed (note the trailing '*')
dpkg -l sendmail*
# Remove it if installed
apt purge sendmail*
# Install and configure postfix
apt install postfix
dpkg-reconfigure postfix --priority low

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
* https://github.com/backuppc/backuppc/releases/
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
/usr/local/bin/rsync_bpc --version
perl -e 'use lib "/usr/local/BackupPC/lib"; use BackupPC::Lib; use BackupPC::XS; print $BackupPC::XS::VERSION'
# Search for string like "# Version 4.3.0, released 25 Nov 2018." in /usr/local/BackupPC/bin/BackupPC
```

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
# [!] When installing, use this. Change '--hostname backuppc' to the actual host name
# ./configure.pl --batch --cgi-dir /var/www/cgi-bin/BackupPC --data-dir /var/lib/backuppc \
#   --hostname $(hostname -f) --html-dir /var/www/html/BackupPC --html-dir-url /BackupPC \
#   --install-dir /usr/local/BackupPC

# When upgrading, use this instead:
service backuppc stop
./configure.pl --batch --config-path /etc/BackupPC/config.pl
service backuppc start
```
Only for new installation, skip this for upgrade
```shell
# The following is good also when upgrading, unless the file contains custom modifications.
# Allows to connect to web UI from anywhere, not only from 127.0.0.1 by removing the following lines:
# order deny,allow
# deny from all
# allow from 127.0.0.1
cp httpd/BackupPC.conf /etc/apache2/conf-available/backuppc.conf
sed -i "/deny\ from\ all/d" /etc/apache2/conf-available/backuppc.conf
sed -i "/deny\,allow/d" /etc/apache2/conf-available/backuppc.conf
sed -i "/allow\ from/d" /etc/apache2/conf-available/backuppc.conf

cp /etc/apache2/envvars{,.bak}
# Note that changing the apache user and group (next two commands) could cause other services
# provided by apache to fail. There are alternatives if you don't want to change the apache
# user: use SCGI or a setuid BackupPC_Admin script - see the docs.
sed -i "s/export APACHE_RUN_USER=www-data/export APACHE_RUN_USER=backuppc/" /etc/apache2/envvars
sed -i "s/export APACHE_RUN_GROUP=www-data/export APACHE_RUN_GROUP=backuppc/" /etc/apache2/envvars

cp /var/www/html/index.html{,.bak}
echo '<html><head><meta http-equiv="refresh" content="0; url=/BackupPC_Admin"></head></html>' > /var/www/html/index.html

a2enconf backuppc
a2enmod cgid
service apache2 restart

cp systemd/backuppc.service /etc/systemd/system
sed -i "s/#Group=backuppc/Group=backuppc/" /etc/systemd/system/backuppc.service
systemctl daemon-reload
systemctl enable backuppc.service

chmod u-s /var/www/cgi-bin/BackupPC/BackupPC_Admin
touch /etc/BackupPC/BackupPC.users
cp /etc/BackupPC/config.pl{,.bak}
nano /etc/BackupPC/config.pl
# Replace
#    $Conf{CgiAdminUserGroup} = '';
#    $Conf{CgiAdminUsers}     = '';
# with
#    $Conf{CgiAdminUserGroup} = 'backuppc';
#    $Conf{CgiAdminUsers}     = 'backuppc';

chown -R backuppc:backuppc /etc/BackupPC

htpasswd /etc/BackupPC/BackupPC.users backuppc

service backuppc start

# Configure mail delivery
# Add alias for backuppc user
nano /etc/aliases
newaliases
# Or change in 'Edit Config' > 'Email' > 'EMailAdminUserName' ($Conf{EMailAdminUserName} in /etc/BackupPC/config.pl)
```

### Maintenance
```shell
# Check email delivery
# [!] as user backuppc
/usr/local/BackupPC/bin/BackupPC_sendEmail -u user[@domain.tld]
# or stop backuppc service and then run
/usr/local/BackupPC/bin/BackupPC_sendEmail -c
# It will check if BackupPC is running, and should send an email to $Conf{EMailAdminUserName} if it is not
# [!] Don't forget to start backuppc service back

# delete an entire backup, or a directory path within a backup
/usr/local/BackupPC/bin/BackupPC_backupDelete

# Try this (add a space after the share name, and add quotes around the path
# since it contains a space):
./BackupPC_backupDelete -h n6850.local -n 4 -s Backup-Data-Folder "/Time Machine"
```
* Re: [BackupPC-users] delete backup: https://sourceforge.net/p/backuppc/mailman/message/35851832/
* Delete files from Backups: https://sourceforge.net/p/backuppc/mailman/message/36287909/

### Client config
```
visudo -f /etc/sudoers.d/backuppc
```
`/etc/sudoers.d/backuppc` content
```
# Allow backuppc to read files with rsync over SSH
backuppc ALL=NOPASSWD: /usr/bin/rsync
```
