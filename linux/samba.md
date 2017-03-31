* https://samba.ninja/2016/10/ubuntu-16-04-samba-ad-member-server/
* https://samba.ninja/2015/10/centos-7-samba-ad-member-server/
* https://samba.ninja/2014/10/ubuntu-14-samba-ad-member-server/
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
smbpasswd –a <username>
# Test smb.conf
testparm
testparm -s
# View tdbsam user list (-v: verbose)
sudo pdbedit -L -v
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
# Install packages
apt update
apt install samba smbclient winbind libnss-winbind libpam-winbind

# Make sure that NTP syncs time with a DC
systemctl status systemd-timesyncd --no-pager -l

# Install Heimdal Kerberos:
apt install heimdal-clients

# Test Kerberos authentication with a domain admin account
# Enter your AD administrator password when prompted, it should just return to command prompt
kinit administrator
# Show your Kerberos ticket for administrator@TEST.LOCAL
klist

# Update /etc/nsswitch.conf to pull users and groups from Winbind
cp /etc/nsswitch.conf{,.bak}
sed -i 's/passwd:\s*compat/passwd: compat winbind/' /etc/nsswitch.conf
sed -i 's/group:\s*compat/group:  compat winbind/' /etc/nsswitch.conf

cp /etc/samba/smb.conf{,.bak}
```
Set `/etc/samba/smb.conf` to the following (ensuring you replace the bold TEST and TEST.LOCAL with your own AD NetBIOS and domain names):
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
```

`/etc/krb5.conf`:
```
[logging]
    default = FILE:/var/log/krb5libs.log
    kdc = FILE:/var/log/krb5kdc.log
    admin_server = FILE:/var/log/kadmind.log

[libdefaults]
    default_realm = GUR.LOCAL
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

[realms]
        GUR.LOCAL = {
                kdc = AD-KGD-01.GUR.local
        }
```

Source:
* https://samba.ninja/2016/10/ubuntu-16-04-samba-ad-member-server/
* https://samba.ninja/2015/10/centos-7-samba-ad-member-server/
