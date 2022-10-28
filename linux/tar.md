Compare speed with lz4: https://stackoverflow.com/questions/24063846/how-to-use-tar-with-lz4
```shell
tar --selinux --acls --xattrs  -cvf file.tar /path/to/a/dir/

tar cvf - directory/ 
ssh user@host "cat /path/to/archive.tar.gz" | tar -xzv
tar cvf - /with/full/path | pigz | ssh -p 12345 -i npa_openssh.key user@host "cd /path; tar xzf -"

# Fix "socket ignored" and subsequent "Exiting with failure status due to previous errors" when
# copying whole filesystems.
# "socket ignored" error is harmless, but to make sure other errors don't creep in, sockets could be excluded.
# Excluding '/dev' also is a good idea
find directory/ -type s -print > /tmp/sockets-to-exclude
tar --exclude=directory/dev/* -X /tmp/sockets-to-exclude -cvf - directory/ | pigz > /path/to/archive.tar.gz
```
