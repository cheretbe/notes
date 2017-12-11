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

:: If PATH already ends with a ";" don't add an extra one
IF "%PATH:~-1%"==";" (
  SET PATH=%PATH%%HOMEDRIVE%%HOMEPATH%\subdir
) ELSE (
  SET PATH=%PATH%;%HOMEDRIVE%%HOMEPATH%\subdir
)
```
