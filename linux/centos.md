* https://unix.stackexchange.com/questions/273327/restart-service-after-yum-update/448755#448755

```shell
# Find which package provides specific file
yum whatprovides '*filename'

# Query packages, provided by a specific repo
yum repolist
yum --disablerepo="*" --enablerepo="*epel" list available

# List files, provided by a specific package
yum install yum-utils
repoquery --list packege-name

# List files, provided by a specific package, without installing it
# 1. Download a package
yum install yum-plugin-downloadonly
yum install --downloadonly --downloaddir . yum-cron
# 2. List files
# -q, --query       command
# -l, --list        list files in package
# -p, --package     query/verify a package file
# -v, --verbose     provide more detailed output
rpm -qlpv yum-cron-3.4.3-168.el7.centos.noarch.rpm
```
