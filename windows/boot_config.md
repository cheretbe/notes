## Repair
* http://woshub.com/how-to-repair-uefi-bootloader-in-windows-8/
* http://pcsupport.about.com/od/fixtheproblem/ht/rebuild-bcd-store-windows.htm
* http://superuser.com/questions/460762/how-can-i-repair-the-windows-8-efi-bootloader

#### MBR to GPT conversion

* https://docs.microsoft.com/en-us/windows/deployment/mbr-to-gpt#disk-prerequisites

Shrink and move system partition to free up 100MiB (204800 sectors) between it and the bootable partition

```batch
powershell Get-PhysicalDisk

:: /disk:<n> - Specifies the disk number of the disk to be processed.
::             If not specified, the system disk is processed.
:: /allowFullOS
::           - Allows the tool to be used from the full Windows
::             environment. By default, this tool can only be used
::             from the Windows Preinstallation Environment.
mbr2gpt /disk:0 /validate /allowFullOS

mbr2gpt /disk:0 /convert /allowFullOS

:: View logs in case of errors
:: Use  /logs:<logDirectory> option to change directory for logging
notepad "%WINDIR%\setupact.log"
notepad "%WINDIR%\setuperr.log"
```

#### Fix BSOD after changing SATA <--> IDE

* `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Msahci`: Set `Start` to `0`
* `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\Pciide`: Set `Start` to `0`

#### Registry keys locations (for offline access):

* https://github.com/cheretbe/notes/blob/master/windows/registry.md#registry-keys-locations-for-offline-access

## Bootable USB
* **https://www.howtogeek.com/196817/how-to-create-a-windows-to-go-usb-drive-without-the-enterprise-edition/**
* https://neosmart.net/wiki/fix-mbr/
* https://sites.google.com/site/godunder/windows-build-files/how-to-create-a-custom-winpe-8-winpe-8-1-5-0-5-1-boot-cd-iso-or-usb-boot-key
* https://www.aomeitech.com/pe-builder.html
* https://www.nextofwindows.com/how-to-re-create-a-bootable-iso-from-extracted-windows-installation-files/

#### Windows To Go
```shell
# Make sure the MBR is clean
dd if=/dev/zero of=/dev/sdX bs=512 count=2
```
* Windows Disk Management
    * Create partition table and NTFS partition
    * Mark it active

Download and run GImageX: https://www.autoitconsulting.com/site/software/gimagex/

* Select "Apply" tab.
    * source: `sources\install.wim`
    * Destination: USB drive letter
    * Select "Check" just in case
* Click "Apply" button

```batch
:: Change to USB drive letter
X:
cd Windows\system32
:: [!] Replace X two times :)
bcdboot.exe X:\Windows /s X: /f ALL
```

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
