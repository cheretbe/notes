# Fix wrong `/var/opt/gitlab` mountpoint

Procedure for the case where a dedicated disk was mistakenly mounted at `/opt/gitlab` instead of `/var/opt/gitlab`. The goal is to swap the contents and remount the disk at the correct path without losing data.

## 0. Check sizes

```bash
lsblk
df -h /opt/gitlab /var/opt/gitlab /
```

## 1. Verify `/` has space for `/opt/gitlab` contents

```bash
du -sh /opt/gitlab --exclude=lost+found
df -h /
```

**STOP** if not enough space.

## 2. Verify disk has space for `/var/opt/gitlab`

```bash
du -sh /var/opt/gitlab
df -h /opt/gitlab
```

**STOP** if not enough space.

## 3. Stop GitLab

```bash
gitlab-ctl stop
systemctl stop gitlab-runsvdir
lsof +D /var/opt/gitlab
lsof +D /opt/gitlab
```

## 4. Take a hypervisor snapshot

## 5. Save `/opt/gitlab` contents to `/`

```bash
rsync -av --info=progress2 /opt/gitlab/ /tmp/opt-gitlab-orig/
```

## 6. Wipe disk, copy `/var/opt/gitlab` onto it (still mounted at `/opt/gitlab`)

```bash
rm -rf /opt/gitlab/*
rsync -av --info=progress2 /var/opt/gitlab/ /opt/gitlab/
```

## 7. Verify

```bash
diff <(cd /var/opt/gitlab && find . | sort) \
     <(cd /opt/gitlab && find . | sort)
```

## 8. Remount disk at `/var/opt/gitlab`

```bash
umount /opt/gitlab
rm -rf /var/opt/gitlab
mkdir /var/opt/gitlab
vi /etc/fstab   # change /opt/gitlab -> /var/opt/gitlab
mount /var/opt/gitlab
```

## 9. Restore `/opt/gitlab`

```bash
rmdir /opt/gitlab
mv /tmp/opt-gitlab-orig /opt/gitlab
```

## 10. Verify and start

```bash
mount | grep var/opt/gitlab
ls /var/opt/gitlab/
ls /opt/gitlab/
systemctl start gitlab-runsvdir
gitlab-ctl reconfigure
gitlab-ctl start
gitlab-ctl status
gitlab-rake gitlab:check
```
