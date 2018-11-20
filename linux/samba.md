* https://samba.ninja/2018/08/ubuntu-18-active-directory-member-server/
* ~~https://samba.ninja/2016/10/ubuntu-16-04-samba-ad-member-server/~~
* ~~https://samba.ninja/2015/10/centos-7-samba-ad-member-server/~~
* ~~https://samba.ninja/2014/10/ubuntu-14-samba-ad-member-server/~~
* https://samba.ninja/2013/12/centos-6-samba-active-directory-member-server/
* https://samba.ninja/2014/10/ubuntu-14-samba-active-directory-member-server/
* https://community.spiceworks.com/topic/157949-only-allow-certain-ad-groups-to-log-in

### Useful commands
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
# Test smb.conf
testparm
testparm -s
# View tdbsam user list (-v: verbose)
sudo pdbedit -L -v
```

### Executable bit
```
# Allow execute files
acl allow execute always = yes
```

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
apt update
apt install samba smbclient winbind libnss-winbind libpam-winbind

# Make sure that NTP syncs time with a DC
systemctl status systemd-timesyncd --no-pager -l

# Update /etc/nsswitch.conf to pull users and groups from Winbind
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
