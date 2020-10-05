Windows
```bat
"C:\Program Files\Git\usr\bin\find.exe" Favorites -not -path "Favorites/Links/*" -type f -exec md5sum -b {} ; | tee d:\temp\md5sum.txt
:: or
cd Favorites
"C:\Program Files\Git\usr\bin\find.exe" . -not -path "./Links/*" -type f -exec md5sum -b {} ; | tee d:\temp\md5sum.txt

:: Check md5 sums
md5sum -c d:\temp\md5sum.txt
:: Don't print OK for each successfully verified file
md5sum -c d:\temp\md5sum.txt --quiet
```
Linux
```shell
find . -type f -not -path "./sync/*" -exec md5sum -b {} \; | tee /mnt/data/temp/md5sum.txt
```
