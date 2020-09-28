* https://www.microsoft.com/en-us/download/details.aspx?id=11533
* https://en.wikibooks.org/wiki/File_Checksum_Integrity_Verifier_(FCIV)_Examples
* https://docs.microsoft.com/en-us/troubleshoot/windows-server/windows-security/fciv-availability-and-description


```shell
LANG=ru_RU.UTF-8 wine cmd
```
* :warning: output XML file is updated, not overwritten
* :warning: "Errors have been reported to fciv.err" is displayed regardless of errors presence. Just check the file contents every time
```batch
:: Create index
c:\fciv\fciv.exe -add c:\windows -r -bp c:\windows -exc c:\temp\exclude.txt -xml c:\temp\index.xml
:: Check files
cd c:\windows
c:\fciv\fciv.exe -v -xml c:\temp\index.xml
```
exclude file example (:warning: Note trailing `<cr><lf>` at the end of file)
```
c:\windows\syswow64

```
