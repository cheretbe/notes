Existing installation (2check): https://www.sevenforums.com/tutorials/87555-user-profile-change-default-location.html<br>
At least this should work (also check): Default user profile location for newly created accounts  `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList` > `ProfilesDirectory`


* Instead of typing username and computer name, enter audit mode (**CTRL+SHIFT+F3**)
* Format drive D:
* Create D:\relocate.xml with the following content  
  (relocation of ProgramData with `<ProgramData>d:\ProgramData</ProgramData>` breaks Metro UI applications, including PC settings and Windows Update)
``` xml
<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
  <settings pass="oobeSystem">
    <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <FolderLocations>
        <ProfilesDirectory>d:\Users</ProfilesDirectory>
      </FolderLocations>
    </component>
  </settings>
  <cpi:offlineImage cpi:source="wim:E:/sources/install.wim#Windows 8.1 PROFESSIONAL" xmlns:cpi="urn:schemas-microsoft-com:cpi" />
</unattend>
```
* Change processorArchitecture="amd64" to "x86" and cpi:source="wim:**E:**/sources/install.wim#**Windows 8.1 PROFESSIONAL**" to HOMEBASIC, HOMEPREMIUM, PROFESSIONAL, ULTIMATE or ENTERPRISE if needed
    * `dism.exe /Get-ImageInfo /imagefile:e:\sources\install.wim`
    * Make sure the file has UTF-8 encoding
* Run sysprep.exe
``` batch
cd %SystemRoot%\System32\Sysprep
sysprep.exe /audit /reboot /unattend:D:\relocate.xml
```
* Windows updates don't install in audit mode (at least on win8.1)  
  Use PSWindowsUpdate (make sure you run `powershell -ExecutionPolicy Unrestricted`)  
  Download PSWindowsUpdate
``` powershell
New-Item -ItemType Directory -Path 'c:\temp\' | Out-Null
Invoke-WebRequest -Uri 'https://225c40b6fb6f3c94f9d5a6b1d51e6941d0474521.googledrive.com/host/0Bw7oiu8ys_I7TTJWQ2lxM2pBQmc/util/PSWindowsUpdate.zip' -OutFile 'c:\temp\PSWindowsUpdate.zip'
Unblock-File -Path 'C:\temp\PSWindowsUpdate.zip'
Add-Type -AssemblyName 'System.IO.Compression.FileSystem'
[System.IO.Compression.ZipFile]::ExtractToDirectory('C:\temp\PSWindowsUpdate.zip', 'C:\temp\')
```
  Install updates  
Skip Malicious Software Removal Tool: `-NotKBArticleID @('KB890830')`
``` powershell
(New-Object -ComObject Microsoft.Update.ServiceManager -Strict).AddService2("7971f918-a847-4430-9279-4a52d1efe18d", 7, "") | Out-Null
# on PS < 3.0 only (e.g. Windows 7)
If (@(Get-Command Unblock-File*).Count -Eq 0)
  { Function Unblock-File {} }
Import-Module C:\temp\PSWindowsUpdate\PSWindowsUpdate.psm1
Get-WUInstall -CategoryIDs @('28bc880e-0592-4cbf-8f95-c79b17911d5f', '0fa1201d-4330-4fa8-8ae9-b877473b6441', 'e6cf1350-c01b-414d-a61f-263d14d133b4') -Confirm:$FALSE
```
* Delete `%SYSTEMROOT%\SoftwareDistribution\Download` contents and cleanup component store
```
Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase
```
* Install everything else what is needed


Source:

http://www.sevenforums.com/tutorials/124198-user-profiles-create-move-during-windows-7-installation.html

Detailed instructions: 
http://www.sevenforums.com/attachments/tutorials/119213d1291161650-user-profiles-create-move-during-windows-7-installation-relocate-user-folders-during-windows-7-installation.pdf
