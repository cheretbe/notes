```bat
dism.exe /Get-ImageInfo /ImageFile:c:\path\to\iso\contents\install.wim
:: or
dism.exe /Get-WimInfo /WimFile:install.wim

:: When used with the /Index or /Name options, more detailed information
:: about the specified image is displayed
dism.exe /Get-WimInfo /WimFile:install.wim /Index:1
dism.exe /Get-ImageInfo /ImageFile:install.wim "/Name:Windows 10 Enterprise LTSC"
```
