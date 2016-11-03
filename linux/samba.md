https://samba.ninja/2016/10/ubuntu-16-04-samba-ad-member-server/
https://samba.ninja/2015/10/centos-7-samba-ad-member-server/
https://samba.ninja/2014/10/ubuntu-14-samba-ad-member-server/

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
```
# Change workgroup and description
workgroup = TEST
server string = %h server (Samba, Ubuntu)

# follow symlincs settings
[global]
follow symlinks = yes
wide links = yes
unix extensions = no

# Шара с аутентификацией (по умолчанию tdbsam)
# Нужно задать пароль командой: sudo smbpasswd -a <username>
# Пользователь должен иметь права на чтение или запись каталога
[test]
  path = /samba/test
  # Группы: @groupname
  read list = npa
  write list = npa
  read only = No
  create mask = 0665
  # Чтобы это работало, нужно установить глобальный параметр
  # obey pam restrictions = no
  force create mode = 0665
  force directory mode = 0775
# Чтобы нормально работали атрибуты файлов с программами типа xcopy
# или robocopy, нужно в fstab включить опцию user_xattr(?) и добавить
# параметры
  ea support = yes
  store dos attributes = yes
  map system = no
  map archive = no
  map readonly = no

# Анонимная шара (установить владельца каталога nobody:nogroup)
[Anonymous]
comment = Anonymous share
path = /samba/anonymous
writable = yes
guest ok = yes
read only = no
create mask = 0665
directory mask = 0775

# Домашние каталоги пользователей
[homes]
  comment = Home Directories
  valid users = %S
  read only = No
  create mask = 0700
  directory mask = 0700
```
