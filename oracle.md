```shell
# [!] The image is huge (11+ GB) plus it uses space at runtime (~16 GB in total)
docker run -d -e ORACLE_PWD=pwd --name oracle container-registry.oracle.com/database/express:latest
# Then use `rlwrap sqlplus`
docker exec -it oracle bash

# rlwrap installation (Oracle Linux Server 7)
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install rlwrap

# for arrows to work in sqlplus use rlwrap
rlwrap sqlplus
```

```sql
-- sqlplus settings
set wrap off;
```
