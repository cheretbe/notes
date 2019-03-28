```shell
# Find which package provides specific file
yum whatprovides '*filename'

# Query packages, provided by a specific repo
yum repolist
yum --disablerepo="*" --enablerepo="*epel" list available
```
