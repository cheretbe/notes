* https://wiki.archlinux.org/title/Davfs2
* :warning: Secrets file format is described in `/etc/davfs2/secrets`
* **TODO:** Try systemd mounting (https://wiki.archlinux.org/title/Davfs2, `Using systemd` section)

Secrets file entry example
```
# Special characters in passwords such as \ and " must be escaped with \
/mnt/dir username password
```

```shell
# [!] The file /sbin/mount.davfs must have the SUID bit set if you want to allow unprivileged (non-root) users to mount WebDAV resources
# To change later use dpkg-reconfigure davfs2
apt install davfs2

# Allow an ordinary user to mount on demand
usermod -aG davfs2 <username>
# /etc/fstab should contain an entry with user,noauto options 
# https://host.domain.tld:1234/seafdav /mnt/dir davfs user,rw,noauto 0 0
# A user needs ~/.davfs2/secrets file with correct permissions (user:user 600) present
# to be able to mount without entering credentials

# Auto-mount on boot
# /etc/fstab entry
# https://host.domain.tld:1234/seafdav /mnt/dir davfs defaults,uid=username,gid=groupname,_netdev,auto 0 0
# For root user credentials will be read from /etc/davfs2/secrets
```
