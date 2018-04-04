## Misc

* Shell Commands: https://winaero.com/blog/list-of-shell-commands-in-windows-10/

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

## Installation from a USB drive

```batch
:: Prepare partition
DISKPART
:: View disks
LIST DISK
:: Select the drive and format it as NTFS
SELECT DISK <N>
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
Get-AppxPackage -AllUsers | Select Name,PackageFamilyName,InstallLocation
```
4) :grey_question: Delete files:  
TODO: Fix directory name
```
SetACL -on "C:\Program Files\WindowsApps\DeletedAllUserPackages" -ot file -actn setowner -ownr "n:S-1-5-32-544" -rec cont_obj
SetACL -on "C:\Program Files\WindowsApps\DeletedAllUserPackages" -ot file -actn ace -ace "n:S-1-5-32-544;p:full" -rec cont_obj
```
### Add Safe Mode to the Windows 8 and 10 Boot Menu
http://www.howtogeek.com/245175/how-to-add-safe-mode-to-the-windows-8-and-10-boot-menu/
