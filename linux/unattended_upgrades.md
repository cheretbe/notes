### Ubuntu

1. Find origin (o=) and archive (a=) of the repository
```shell
# List files
ls /var/lib/apt/lists/*Release

# for GitLab CE
head /var/lib/apt/lists/packages.gitlab.com_gitlab_gitlab-ce_ubuntu_dists_xenial_InRelease
# Origin: packages.gitlab.com/gitlab/gitlab-ce

# for Yandex Disk
head /var/lib/apt/lists/repo.yandex.ru_yandex-disk_deb_dists_stable_InRelease
# Origin: Yandex Disk Archive
```
Archive may not be present

2. Update `/etc/apt/apt.conf.d/50unattended-upgrades`. Allowed origins are separated
in the config file by spaces or colons. If archive (a=) is empty, use colon.
```
Unattended-Upgrade::Allowed-Origins {
//      ...
        "${distro_id}:${distro_codename}-updates";
//      "${distro_id}:${distro_codename}-proposed";
//      "${distro_id}:${distro_codename}-backports";
        "Yandex Disk Archive:";
        "packages.gitlab.com/gitlab/gitlab-ce:${distro_codename}";
};
```

3. Test settings
```shell
unattended-upgrade --debug --dry-run
```

* https://www.richud.com/wiki/Ubuntu_Enable_Automatic_Updates_Unattended_Upgrades
