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

# for Yandex Disk
head /var/lib/apt/lists/repo.yandex.ru_yandex-disk_deb_dists_stable_InRelease
# Origin: Yandex Disk Archive
# Codename: stable
```

3. Update `/etc/apt/apt.conf.d/50unattended-upgrades`
```
Unattended-Upgrade::Allowed-Origins {
//      ...
        "${distro_id}:${distro_codename}-updates";
//      "${distro_id}:${distro_codename}-proposed";
//      "${distro_id}:${distro_codename}-backports";
        "Yandex Disk Archive:stable";
        "packages.gitlab.com/gitlab/gitlab-ce:${distro_codename}";
};

//Uncomment and change to "true"
//Unattended-Upgrade::Remove-Unused-Dependencies "false";

// [!] Make sure update-notifier-common package is installed for the following to work
//Unattended-Upgrade::Automatic-Reboot "false";
//Unattended-Upgrade::Automatic-Reboot-Time "02:00";
```

4. Test settings
```shell
unattended-upgrade --debug --dry-run
```

* https://www.richud.com/wiki/Ubuntu_Enable_Automatic_Updates_Unattended_Upgrades
* https://linux-audit.com/upgrading-external-packages-with-unattended-upgrade/
* (:warning: - see comments) https://linux-audit.com/upgrading-external-packages-with-unattended-upgrade/
