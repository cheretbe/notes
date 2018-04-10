```shell
# create archive
7z a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on archive.7z /path/to/files
# test archive
7z t archive.7z
```
* https://superuser.com/questions/281573/what-are-the-best-options-to-use-when-compressing-files-using-7-zip
