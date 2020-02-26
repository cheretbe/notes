## Unsorted

Show desktop shortcut: `%windir%\explorer.exe shell:::{3080F90D-D7AD-11D9-BD98-0000947B0257}`<br>
Icon file: `%windir%\explorer.exe`

boot-time Chkdsk results: "Application" log, event source "Wininit"

[New wallpaper](../files/windows/Windows10_1903_4K_wallpaper.zip) ([direct link](https://github.com/cheretbe/notes/raw/master/files/windows/Windows10_1903_4K_wallpaper.zip)) for 1080p use 3840x2160, it's 16:9

KMS activation
```batch
:: In the Office dir (e.g. C:\Program Files\Microsoft Office\Office14):
cscript ospp.vbs /sethst:kms.domain.tld
cscript ospp.vbs /setprt:portno
cscript ospp.vbs /act
:: Check license status
cscript ospp.vbs /dstatus

script slmgr.vbs -skms kms.domain.tld:portno
cscript slmgr.vbs -ato
:: Check status
cscript slmgr.vbs -dlv
cscript slmgr.vbs -xpr
```

```batch
:: Disable hibernation
powercfg /h off
:: Network trace
netsh trace start capture=yes scenario=netconnection maxsize=1024 tracefile=C:\%computername%.etl
```

WinSxS store cleanup
```batch
:: Analyze
Dism.exe /Online /Cleanup-Image /AnalyzeComponentStore
:: Cleanup
Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase
```

`control userpasswords2` encrypted password uses  LsaStorePrivateData?
* https://www.snip2code.com/Snippet/1080596/Auto-Logon-Script-for-Windows
* https://andyarismendi.blogspot.ru/2011/10/powershell-set-secureautologon.html

Shell Commands:
```
start shell:Desktop
```
* https://winaero.com/blog/list-of-shell-commands-in-windows-10/

Shadow copies
```
vssadmin list shadows
vssadmin delete shadows /all
```
Exclusions are in `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\BackupRestore\FilesNotToSnapshot`

Change environment variables as standard user
```
rundll32 sysdm.cpl,EditEnvironmentVariables
```

Profile list
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\
```

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

Kill freezed service
```batch
:: Find PID of the service process
sc queryex <service name>

:: Kill process
taskkill [/f] /PID <PID>

:: Kill all running exe instances:
taskkill [/f] /IM <exe name>

:: List running exe instances:
tasklist /v /fi "Imagename eq robocopy.exe"
```

## Fix BSOD after changing SATA <--> IDE

* `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Msahci`: Set `Start` to `0`
* `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Pciide`: Set `Start` to `0`

Registry keys locations (for offline access):
* HKEY_LOCAL_MACHINE\SYSTEM - `%windir%\system32\config\system`
* HKEY_LOCAL_MACHINE\SOFTWARE - `%windir%\system32\config\software`
* HKEY_USERS\\.Default - `%windir%\system32\config\default`
* HKEY_CURRENT_USER - `%userprofile%\ntuser.dat`

## Installation from a USB drive

```batch
:: Prepare partition
DISKPART
:: View disks
LIST DISK
:: Select the drive and format it as NTFS
SELECT DISK <N>
:: Verify that the correct drive has been selected
DETAIL DISK
CLEAN
CREATE PARTITION PRIMARY
SELECT PARTITION 1
ACTIVE
FORMAT FS=NTFS quick
ASSIGN
EXIT

:: Make drive bootable
CD BOOT
BOOTSECT.EXE /NT60 <drive letter>:

:: Copy installation files to the root of the drive
```
* https://www.howtogeek.com/196817/how-to-create-a-windows-to-go-usb-drive-without-the-enterprise-edition/
* https://neosmart.net/wiki/fix-mbr/

## Fixes for Errors in Logs

1. Source: **Store-Licensing**, Event ID: **512**
    - `Windows Store failed to sync machine licenses. Result code 0x80070002)`
```
schtasks /change /disable /tn "\Microsoft\Windows\WS\WSRefreshBannedAppsListTask"
```
2. Source: **DistributedCOM**, Event ID: **10010**
    - `The server {BF6C1E47-86EC-4194-9CE5-13C15DCB2001} did not register with DCOM within the required timeout.`
    - `The server {1B1F472E-3221-4826-97DB-2C2324D389AE} did not register with DCOM within the required timeout.`
```
schtasks /change /disable /tn "\Microsoft\Windows\SkyDrive\Idle Sync Maintenance Task"
schtasks /change /disable /tn "\Microsoft\Windows\SkyDrive\Routine Maintenance Task"
```



## Remove Windows Store Apps
1) From system account:
```
Get-AppXProvisionedPackage -online | Remove-AppxProvisionedPackage -online
```
2) For all users:

~~`Get-AppxPackage -AllUsers | Remove-AppxPackage`~~
```powershell
# Win8.1 only
Get-AppxPackage -AllUsers | Where-Object Name -eq "Microsoft.SkypeApp" | Remove-AppxPackage
# Win8.1/10
Get-AppxPackage -AllUsers | Where-Object PublisherId -eq "8wekyb3d8bbwe" | Remove-AppxPackage
```
* https://support.microsoft.com/en-us/help/2769827/sysprep-fails-after-you-remove-or-update-windows-store-apps-that-inclu
* https://superuser.com/questions/533170/how-to-fully-uninstall-a-windows-store-app/533220#533220
3) Selective deletion
```powershell
Get-AppxPackage -AllUsers | Select Name,PackageFamilyName,InstallLocation | Out-GridView
```
4) :grey_question: Delete files:  
TODO: Fix directory name
```
SetACL -on "C:\Program Files\WindowsApps\DeletedAllUserPackages" -ot file -actn setowner -ownr "n:S-1-5-32-544" -rec cont_obj
SetACL -on "C:\Program Files\WindowsApps\DeletedAllUserPackages" -ot file -actn ace -ace "n:S-1-5-32-544;p:full" -rec cont_obj
```
### Add Safe Mode to the Windows 8 and 10 Boot Menu
http://www.howtogeek.com/245175/how-to-add-safe-mode-to-the-windows-8-and-10-boot-menu/
