## Repair
* http://woshub.com/how-to-repair-uefi-bootloader-in-windows-8/
* http://pcsupport.about.com/od/fixtheproblem/ht/rebuild-bcd-store-windows.htm
* http://superuser.com/questions/460762/how-can-i-repair-the-windows-8-efi-bootloader

#### Fix BSOD after changing SATA <--> IDE

* `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Msahci`: Set `Start` to `0`
* `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Pciide`: Set `Start` to `0`

Registry keys locations (for offline access):
* HKEY_LOCAL_MACHINE\SYSTEM - `%windir%\system32\config\system`
* HKEY_LOCAL_MACHINE\SOFTWARE - `%windir%\system32\config\software`
* HKEY_USERS\\.Default - `%windir%\system32\config\default`
* HKEY_CURRENT_USER - `%userprofile%\ntuser.dat`

## Bootable USB
* **https://www.howtogeek.com/196817/how-to-create-a-windows-to-go-usb-drive-without-the-enterprise-edition/**
* https://neosmart.net/wiki/fix-mbr/
* https://sites.google.com/site/godunder/windows-build-files/how-to-create-a-custom-winpe-8-winpe-8-1-5-0-5-1-boot-cd-iso-or-usb-boot-key
* https://www.aomeitech.com/pe-builder.html
* https://www.nextofwindows.com/how-to-re-create-a-bootable-iso-from-extracted-windows-installation-files/

#### Installation from a USB drive

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
