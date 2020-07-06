* https://wiki.debian.org/AuthenticatingLinuxWithActiveDirectorySssd
* https://samba.ninja/2018/08/ubuntu-18-active-directory-member-server/
* ~~https://samba.ninja/2016/10/ubuntu-16-04-samba-ad-member-server/~~
* ~~https://samba.ninja/2015/10/centos-7-samba-ad-member-server/~~
* ~~https://samba.ninja/2014/10/ubuntu-14-samba-ad-member-server/~~
* https://samba.ninja/2013/12/centos-6-samba-active-directory-member-server/
* https://samba.ninja/2014/10/ubuntu-14-samba-active-directory-member-server/
* https://community.spiceworks.com/topic/157949-only-allow-certain-ad-groups-to-log-in

### Misc. info

* No guest access to share list in Windows 10
  * https://support.microsoft.com/en-us/help/4046019/guest-access-in-smb2-disabled-by-default-in-windows-10-and-windows-ser
      * Computer configuration > administrative templates > network > Lanman Workstation: "Enable insecure guest logons"
      * Конфигурация компьютера > Административные шаблоны > Сеть > Рабочая станция Lanman: "Включить небезопасные гостевые входы"
  * or
      * change `map to guest = bad user` to `map to guest = never` in `/etc/samba/smb.conf`
  * or
      * `cmd /c reg query HKLM\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters /v AllowInsecureGuestAuth`
      * `cmd /c reg add HKLM\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters /v AllowInsecureGuestAuth /t REG_DWORD /d 1 /f`

#### Useful commands
``` shell
# Everything as root
# View stats
smbstatus
# Show locks only
smbstatus -L
# For a specific user
smbstatus -u <username>
# Sessions and shares only
net status sessions
net status shares
# List current samba group map to local groups
net groupmap list

# Change password
smbpasswd -a <username>
# List users
# -L to list users, -v to be verbose
sudo pdbedit -L -v

# Test smb.conf
testparm
testparm -s
# View tdbsam user list (-v: verbose)
sudo pdbedit -L -v
```

#### smb.conf
```
[global]
; Allow execute files (executable bit)
acl allow execute always = yes

; https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html#CLIENTMAXPROTOCOL
; default is 'CORE' (MS-DOS era)
client min protocol = CORE
; default is 'NT1' (aka CIFS)
client max protocol = NT1
```

### Client
* SMB dialect versions: https://wiki.samba.org/index.php/SMB3_kernel_status
* Notes on cifs.ko: https://superuser.com/questions/1297724/linux-force-default-mount-cifs-version-to-3-0/1323578#1323578
* If `vers` option is not specified, `mount.cifs` uses `vers=default`, where `default` is hard-coded in `cifs.ko` and therefore depends on kernel version.
```shell
sudo apt install smbclient cifs-utils

sudo mount -t cifs -o username=USERNAME,password=PASSWD,domain=DOMAIN //smb_server/share /mnt/share
# Doesn't work as non-root?
mount -t cifs -o username=USERNAME,password=PASSWD,uid=$USER,gid=$USER //smb_server/share ~/mnt/share

# -o is not needed in /etc/fstab
# https://askubuntu.com/questions/922682/specify-smb-3-0-in-etc-fstab/963907#963907

# ,credentials=/root/.smbcredentials
```
`.smbcredentials` example (domain is optional)
```
username=myusername
password=mypassword
domain=WORKGROUP
```
* :warning: CIFS bug causing SMBv2+ not to show all files/directories
    * https://bugs.launchpad.net/ubuntu/+source/linux/+bug/1572132
    * https://bugzilla.samba.org/show_bug.cgi?id=13107
    * https://serverfault.com/questions/955606/mounted-windows-disk-incomplete-directory-listing
```shell
# Check missing files
# Mount with vers=1.0 and calc checksums
md5deep -r -s /mountpoint > checksums
# Then remount and compare checksums
md5deep -r -X checksums /mountpoint
```

Checking SMB Version used (Windows)
```powershell
# Need to be run as Administrator on client
Get-SmbConnection
# On server
Get-SmbSession | Select-Object -Property *
```
* https://www.itprotoday.com/windows-server/checking-your-smb-version
* https://blogs.technet.microsoft.com/josebda/2013/10/02/windows-server-2012-r2-which-version-of-the-smb-protocol-smb-1-0-smb-2-0-smb-2-1-smb-3-0-or-smb-3-02-are-you-using/


### Standalone server
No LDAP, no Windows domain, local users.
Install `samba` package and edit default `/etc/samba/smb.conf`. Run `testparm` after each edit.
``` ini
# Change workgroup and description
workgroup = TEST
server string = %h server (Samba, Ubuntu)

[global]
# follow symlincs settings
follow symlinks = yes
wide links = yes
unix extensions = no

# Disable printing
load printers = no
printing = bsd
printcap name = /dev/null
disable spoolss = yes

# Allow execute files
acl allow execute always = yes

# Share with authentication (by default it is tdbsam)
# Password has to be set by: sudo smbpasswd -a <username>
# User needs read or write access to the directory
[test]
  path = /samba/test
  # Groups: @groupname
  read list = npa
  write list = npa
  read only = No
  create mask = 0665
  # For this to work the following GLOBAL param has to be set
  # obey pam restrictions = no
  force create mode = 0665
  force directory mode = 0775
# For DOS file attributes to work with programs like xcopy or robocopy
# user_xattr has to be enabled in /etc/fstab and the following parameters
# turned on
# TODO: check if robocopy actually needs this
  ea support = yes
  store dos attributes = yes
  map system = no
  map archive = no
  map readonly = no

# Anonymous share (set directory owner to nobody:nogroup)
[Anonymous]
comment = Anonymous share
path = /samba/anonymous
writable = yes
guest ok = yes
read only = no
create mask = 0665
directory mask = 0775

# Home directories
[homes]
  comment = Home Directories
  valid users = %S
  read only = No
  create mask = 0700
  directory mask = 0700
```

### Domain member

```bash
# Check if DNS is working and host names resolve correctly (especially if domain uses .local TLD)
nslookup dc1.test.local
# If not, make sure there is no Avahi daemon
apt purge avahi-daemon
# Check if systemd-resolved is running and try disabling it
# https://github.com/cheretbe/notes/blob/master/linux/dns+dhcp.md#dns-client
systemd-resolve --status

# Install packages
# smbclient is not needed for a server
apt update
apt install samba krb5-user winbind libnss-winbind libpam-winbind

# Make sure that NTP syncs time with a DC
systemctl status systemd-timesyncd --no-pager -l

# Update /etc/nsswitch.conf to pull users and groups from Winbind
# passwd: compat systemd   =>   passwd: compat winbind systemd
# group:  compat systemd   =>   group:  compat winbind systemd
cp /etc/nsswitch.conf{,.bak}
sed -i 's/passwd:\s*compat/passwd: compat winbind/' /etc/nsswitch.conf
sed -i 's/group:\s*compat/group:  compat winbind/' /etc/nsswitch.conf

cp /etc/samba/smb.conf{,.bak}
echo > /etc/samba/smb.conf
nano /etc/samba/smb.conf
```
Set `/etc/samba/smb.conf` to the following (ensuring you replace the TEST and TEST.LOCAL with your own AD NetBIOS and domain names):
```ini
[global]
    workgroup = TEST
    server string = Samba Server Version %v
    security = ads
    realm = TEST.LOCAL
    socket options = TCP_NODELAY IPTOS_LOWDELAY SO_RCVBUF=131072 SO_SNDBUF=131072
    use sendfile = true
	 
    idmap config * : backend = tdb
    idmap config * : range = 100000-299999
    idmap config TEST : backend = rid
    idmap config TEST : range = 10000-99999
    winbind separator = +
    winbind enum users = yes
    winbind enum groups = yes
    winbind use default domain = yes
    winbind refresh tickets = yes

    restrict anonymous = 2
    log file = /var/log/samba/log.%m
    max log size = 50
		 
#============================ Share Definitions ==============================
		 
[testshare]
    comment = Test share
    path = /samba/testshare
    read only = no
    force group = "Domain Users"
    directory mask = 0770
    force directory mode = 0770
    create mask = 0660
    force create mode = 0660
    
    #valid users = "@local-admins", "@пользователи домена"
    #read list = "@local-admins", "@пользователи домена"
    #write list = "@local-admins"
    #force group = "local-admins"
```
To be able to login as domain user add the following option:
```ini
template shell = /bin/bash
```
```shell
cp /etc/krb5.conf{,.bak}
echo > /etc/krb5.conf
nano /etc/krb5.conf
```
Set `/etc/krb5.conf` to the following:
```
[logging]
    default = FILE:/var/log/krb5libs.log
    kdc = FILE:/var/log/krb5kdc.log
    admin_server = FILE:/var/log/kadmind.log

[libdefaults]
    default_realm = TEST.LOCAL
    ticket_lifetime = 24h
    forwardable = yes

    # tests


[appdefaults]
    pam = {
        debug = true
        ticket_lifetime = 36000
        renew_lifetime = 36000
        forwardable = true
        krb4_convert = false
    }

#[realms]
#        TEST.LOCAL = {
#                kdc = dc1.test.local
#        }
```

```shell
# Test Kerberos authentication with a domain admin account
# Enter your AD administrator password when prompted, it should just return to command prompt
kinit administrator
# Show your Kerberos ticket for administrator@TEST.LOCAL
klist
```


Join your SAMBA server to the domain:
```shell
# Should return:
# Using short domain name -- TEST
# Joined 'SERVER-NAME' to dns domain 'test.local'
# 
# [!] test createcomputer option: createcomputer=Servers/UNIX
net ads join test.local -U administrator

# Should return "OK"
sudo net ads testjoin

# Restart SAMBA services
systemctl restart winbind smbd nmbd

# Test domain join and Winbind AD user/group resolution:
# Should list your AD users
wbinfo -u
# Should list your AD groups
wbinfo -g
# Should list AD users with UIDs in the 10000+ range
getent passwd
# Should list AD groups with UIDS in the 10000+ range
getent group
```

Create the location your SAMBA share will be stored:
```
sudo mkdir -p /samba/testshare
sudo chown administrator:"domain users" /samba/testshare
sudo chmod 0770 /samba/testshare
```

Edit `/etc/pam.d/common-session`, add the following at the bottom of the file. Be careful – mis-editing PAM configuration could permanently lock you out of your system! Take a snapshot before proceeding.
```
# create home directories at first logon
session required   pam_mkhomedir.so skel=/etc/skel/ umask=0077
```
To limit access to sertain groups only, add the following to `/etc/pam.d/common-session`:
```
account required pam_access.so
```
and the following to `/etc/security/access.conf`:
```
-:ALL EXCEPT root local-admin (ad-admins):ALL
```
`/etc/sudoers` entry example
```
# Allow members of domain-admins-group (TEST.local domain) to execute any command
%domain-admins-group       ALL=(ALL:ALL) ALL
%group\ with\ a\ space     ALL=(ALL:ALL) ALL
```


Source:
* https://samba.ninja/2016/10/ubuntu-16-04-samba-ad-member-server/
* https://samba.ninja/2015/10/centos-7-samba-ad-member-server/


:warning: **TODO:** Test sssd variant

* https://www.redhat.com/en/blog/sssd-vs-winbind
* https://sssd.io/docs/users/ad_provider.html
