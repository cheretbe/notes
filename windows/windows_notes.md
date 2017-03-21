## Misc
Clear all event logs
```powershell
# Powershell
wevtutil el | Foreach-Object {wevtutil cl "$_"}
```

Allow access to administrative shares, remote registry and remote management
```batch
:: View current setting. Should be 0x1
reg.exe QUERY HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /v LocalAccountTokenFilterPolicy
:: Update setting
reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 0x1 /f
```

## Fixes for Errors in Logs

1. Source: **Store-Licensing**, Event ID: **512** (Windows Store failed to sync machine licenses. Result code 0x80070002)
```
schtasks /change /disable /tn "\Microsoft\Windows\WS\WSRefreshBannedAppsListTask"
```


## Remove Windows Store Apps
1) From system account:
```
Get-AppXProvisionedPackage -online | Remove-AppxProvisionedPackage -online
```
2) For all users:
```
Get-AppxPackage -AllUsers | Remove-AppxPackage
```
In Windows 10, you should use: `Get-AppXPackage -User <username> | Remove-AppxPackage` (? 2check)

3) Delete files:  
TODO: Fix directory name
```
SetACL -on "C:\Program Files\WindowsApps\DeletedAllUserPackages" -ot file -actn setowner -ownr "n:S-1-5-32-544" -rec cont_obj
SetACL -on "C:\Program Files\WindowsApps\DeletedAllUserPackages" -ot file -actn ace -ace "n:S-1-5-32-544;p:full" -rec cont_obj
```
### Add Safe Mode to the Windows 8 and 10 Boot Menu
http://www.howtogeek.com/245175/how-to-add-safe-mode-to-the-windows-8-and-10-boot-menu/
