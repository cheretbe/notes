* https://www.microsoft.com/en-us/download/details.aspx?id=11533
* https://en.wikibooks.org/wiki/File_Checksum_Integrity_Verifier_(FCIV)_Examples
* https://docs.microsoft.com/en-us/troubleshoot/windows-server/windows-security/fciv-availability-and-description


```shell
LANG=ru_RU.UTF-8 wine cmd
```
```batch
c:\fciv\fciv.exe -add z:\mnt\data\yandexDisk\data\docs -r -bp z:\mnt\data\yandexDisk\data\docs -xml z:\home\orlov\temp\index.xml
c:\fciv\fciv.exe -add c:\windows -r -bp c:\windows -exc c:\temp\exclude.txt -xml c:\temp\index.xml
```
exclude file exampld (:warning: Note trailing <cr><lf> at the end of file)
```
c:\windows\syswow64

```
