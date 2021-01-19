### Ubuntu

1. Install
```shell
apt install unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
```

2. Custom packages. Find origin (o=) and archive (a=) (codename?) of the repository
```shell
# List files
ls /var/lib/apt/lists/*Release

# for GitLab CE (16.04)
head /var/lib/apt/lists/packages.gitlab.com_gitlab_gitlab-ce_ubuntu_dists_xenial_InRelease
# Origin: packages.gitlab.com/gitlab/gitlab-ce
# Codename: xenial

# for Docker
# Origin: Docker
# Suite: bionic

# for Yandex Disk
head /var/lib/apt/lists/repo.yandex.ru_yandex-disk_deb_dists_stable_InRelease
# Origin: Yandex Disk Archive
# Codename: stable
```

3. Update `/etc/apt/apt.conf.d/20auto-upgrades`, adding
```
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
```

4. Update `/etc/apt/apt.conf.d/50unattended-upgrades`
```
Unattended-Upgrade::Allowed-Origins {
//      ...
        "${distro_id}:${distro_codename}-updates";
//      "${distro_id}:${distro_codename}-proposed";
//      "${distro_id}:${distro_codename}-backports";
        "Yandex Disk Archive:stable";
        "packages.gitlab.com/gitlab/gitlab-ce:${distro_codename}";
        "Docker:${distro_codename}";
        "Sublime Text:apt/stable";

        "origin=Raspbian,codename=${distro_codename},label=Raspbian";
        "origin=Raspberry Pi Foundation,codename=${distro_codename},label=Raspberry Pi Foundation";
};

//Uncomment and change to "true"
//Unattended-Upgrade::Remove-Unused-Dependencies "false";

// [!] Make sure update-notifier-common package is installed for the following to work
//Unattended-Upgrade::Automatic-Reboot "false";
//Unattended-Upgrade::Automatic-Reboot-Time "02:00";
```

5. Test settings
```shell
unattended-upgrade --debug --dry-run
# Less verbose output
unattended-upgrade -v --dry-run
```

* https://www.richud.com/wiki/Ubuntu_Enable_Automatic_Updates_Unattended_Upgrades
* https://linux-audit.com/upgrading-external-packages-with-unattended-upgrade/
* (:warning: - see comments) https://linux-audit.com/upgrading-external-packages-with-unattended-upgrade/

### RHEL/CentOS

* https://dnf.readthedocs.io/en/latest/automatic.html
* https://linuxize.com/post/configure-automatic-updates-with-yum-cron-on-centos-7/
* https://www.cyberciti.biz/faq/fedora-automatic-update-retrieval-installation-with-cron/


#### CentOS 7
```shell
yum install yum-cron

# Restart status
needs-restarting  -r
```
* The `yum-cron` service only controls whether or not the cron jobs will run. It is present only to allow
    one to use chkconfig and the standard "service stop|start" commands to enable or disable yum-cron.
* The `yum-cron` utility is called by the `/etc/cron.hourly/0yum-hourly.cron` and `/etc/cron.daily/0yum-daily.cron` cron files
* `/etc/yum/yum-cron-hourly.conf` by default does nothing
* `/etc/yum/yum-cron.conf` (used by the daily cron job) by default only downloads updates when they are available, but doesn't install them.
   Set `apply_updates = no` to install them as well

#### CentOS 8
```shell
dnf install dnf-automatic
# Settings are in /etc/dnf/automatic.conf
nano /etc/dnf/automatic.conf
# Enable timer
systemctl enable --now dnf-automatic-install.timer

# Run dnf-automatic manually to check if everything functions properly
dnf-automatic
# dnf-automatic has no own log, check /var/log/dnf.rpm.log
cat /var/log/dnf.rpm.log
# Restart status
dnf needs-restarting
```

Cron job example
```shell
#!/bin/bash
needs-restarting -r > /dev/null || shutdown -r
```
