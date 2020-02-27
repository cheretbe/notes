Compare speed with lz4: https://stackoverflow.com/questions/24063846/how-to-use-tar-with-lz4
```shell
tar --selinux --acls --xattrs  -cvf file.tar /path/to/a/dir/

tar cvf - directory/ | pigz > /path/to/archive.tar.gz
ssh user@host "cat /path/to/archive.tar.gz" | tar -xzv
tar cvf - /with/full/path | pigz | ssh -p 12345 -i npa_openssh.key user@host "cd /path; tar xzf -"
```
