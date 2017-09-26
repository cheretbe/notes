```bat
IF EXIST "%FileName%" (
  ECHO Deleting existing '%FileName%'
  DEL /Q /F "%FileName%"
)
```
