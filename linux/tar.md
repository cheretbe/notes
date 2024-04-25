Compare speed with lz4: https://stackoverflow.com/questions/24063846/how-to-use-tar-with-lz4 (use lz4mt, compare with pigz)
```shell
tar -czvf file.tar.gz /path/to/a/dir/
tar --selinux --acls --xattrs  -cvf file.tar /path/to/a/dir/

# Target directory
tar xzvf archive.tar.gz --directory extracted/

# Test file integrity
tar -tzf file.tar.gz

# Check if directory is readable
# not "tar cf /dev/null directory/" is because when the archive is being created to /dev/null,
# tar tries to minimize input and output operations.
# https://unix.stackexchange.com/questions/512362/why-does-tar-appear-to-skip-file-contents-when-output-file-is-dev-null
# [!] no -v as we want to see errors only
tar cf - directory/ | cat > /dev/null
# less overhead (?)
tar cf - directory/ | pv -q > /dev/null

ssh user@host "cat /path/to/archive.tar.gz" | tar -xzv
tar cvf - /with/full/path | pigz | ssh -p 12345 -i npa_openssh.key user@host "cd /path; tar xzf -"

# Fix "socket ignored" and subsequent "Exiting with failure status due to previous errors" when
# copying whole filesystems.
# "socket ignored" error is harmless, but to make sure other errors don't creep in, sockets could be excluded.
# Excluding '/dev' and '/swapfile' (if present) also is a good idea
find directory/ -type s -print > /tmp/sockets-to-exclude
tar --exclude=directory/dev/* -X /tmp/sockets-to-exclude -cvf - directory/ | pigz > /path/to/archive.tar.gz
```
