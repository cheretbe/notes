* https://unix.stackexchange.com/questions/273327/restart-service-after-yum-update/448755#448755

```shell
# Find which package provides specific file
yum whatprovides '*filename'

# Query packages, provided by a specific repo
yum repolist
yum --disablerepo="*" --enablerepo="*epel" list available
```
