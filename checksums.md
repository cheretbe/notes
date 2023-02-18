* TODO: check this: https://github.com/rhash/RHash

```shell
# md5deep ==> hashdeep
# [!] There is windows version

#     -r  recursive mode. All subdirectories are traversed
#     -c <alg1,[alg2]> - Compute hashes only. Defaults are MD5 and SHA-256
#                         we use only one hash type for speed. Which is faster, md5 or sha1,
#                         depends on the CPU etc.
# [!] -j <num>  use num threads (default 2)
# [!] -l        print relative paths for filenames
hashdeep -c MD5 -r /mountpoint > checksums

# Audit mode
# The -v flag can be repeated multiple times, up to three times, to get more information on the status of each file.
hashdeep -r -k checksums -a -vv /mountpoint

# Examples
cd /mnt/hdd1/data/temp/photo
hashdeep -c MD5 -r -l . > /mnt/hdd1/data/temp/photo_checksums
cd /path/to/another/copy
hashdeep -r -l -k /mnt/hdd1/data/temp/photo_checksums -a -vv .
```

Windows
```bat
"C:\Program Files\Git\usr\bin\find.exe" Favorites -not -path "Favorites/Links/*" -type f -exec md5sum -b {} ; | tee d:\temp\md5sum.txt
:: or
cd Favorites
"C:\Program Files\Git\usr\bin\find.exe" . -not -path "./Links/*" -type f -exec md5sum -b {} ; | tee d:\temp\md5sum.txt

:: Check md5 sums
:: NOTE:
:: Each file's status lines (including failed ones) are sent to stdout.
:: However, the final warning line (if present) is sent to stderr.
md5sum -c d:\temp\md5sum.txt
:: Don't print OK for each successfully verified file
md5sum -c d:\temp\md5sum.txt --quiet
```
Linux
```shell
find . -type f -not -path "./sync/*" -exec md5sum -b {} \; | tee /mnt/data/temp/md5sum.txt
```
