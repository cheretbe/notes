```bat
IF EXIST "%FileName%" (
  ECHO Deleting existing '%FileName%'
  DEL /Q /F "%FileName%"
)

IF "%ProgramFiles(x86)%"=="" (
  ECHO x86
) ELSE (
  ECHO x64
)
```
