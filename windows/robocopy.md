* https://ss64.com/nt/robocopy.html
* https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy

```batch
:: /R:n : Number of Retries on failed copies - default is 1 million.
:: /W:n : Wait time between retries - default is 30 seconds.
:: /NP  : No Progress - don’t display % copied.
:: /NDL : No Directory List - don’t log directory names.
robocopy "c:\src" "d:\dst" /MIR /R:1 /W:0 /NP /NDL

:: /L : List only - don’t copy, timestamp or delete any files.

IF ERRORLEVEL 8 (
  ECHO ERRORLEVEL: %ERRORLEVEL%
  SET CopyResult=1
) ELSE (
  ECHO ERRORLEVEL: %ERRORLEVEL%
  SET CopyResult=0
)
```
