* https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/call#batch-parameters
```batch
:: [!] Not current directory
ECHO Full path to script's directory: %~dp0

ECHO Full path to the script file: %~f0
ECHO Script file name with no extension: %~n0
```

```bat
echo:Press any key to continue... & pause >NUL

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
  SET "PATH=%PATH%%HOMEDRIVE%%HOMEPATH%\subdir"
) ELSE (
  SET "PATH=%PATH%;%HOMEDRIVE%%HOMEPATH%\subdir"
)

FOR /F "TOKENS=1,2,*" %%A IN ('REG QUERY "HKLM\SOFTWARE\TortoiseSVN" /V "Directory"') DO SET SvnRootDir=%%C
```
