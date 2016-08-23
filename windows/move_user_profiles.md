* Instead of typing username and computer name, enter audit mode (**CTRL+SHIFT+F3**)
* Format drive D:
* Create D:\relocate.xml with the following content
``` xml
<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
  <settings pass="oobeSystem">
    <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <FolderLocations>
        <ProfilesDirectory>d:\Users</ProfilesDirectory>
        <ProgramData>d:\ProgramData</ProgramData>
      </FolderLocations>
    </component>
  </settings>
  <cpi:offlineImage cpi:source="wim:E:/sources/install.wim#Windows 8.1 PROFESSIONAL" xmlns:cpi="urn:schemas-microsoft-com:cpi" />
</unattend>
```
* Change processorArchitecture="amd64" to "x86" and cpi:source="wim:**E:**/sources/install.wim#**Windows 8.1 PROFESSIONAL**" to HOMEBASIC, HOMEPREMIUM, PROFESSIONAL, ULTIMATE or ENTERPRISE if needed
* Run sysprep.exe
``` batch
cd %SystemRoot%\System32\Sysprep
sysprep.exe /audit /reboot /unattend:D:\relocate.xml
```
* Windows updates don't install in audit mode (at least on win8.1)
  Use PSWindowsUpdate
``` powershell
New-Item -ItemType Directory -Path 'c:\temp\' | Out-Null
Invoke-WebRequest -Uri 'https://225c40b6fb6f3c94f9d5a6b1d51e6941d0474521.googledrive.com/host/0Bw7oiu8ys_I7TTJWQ2lxM2pBQmc/util/PSWindowsUpdate.zip' -OutFile 'c:\temp\PSWindowsUpdate.zip'
Unblock-File -Path 'C:\temp\PSWindowsUpdate.zip'
New-Item -ItemType Directory -Path 'c:\temp\PSWindowsUpdate\' | Out-Null
Add-Type -AssemblyName 'System.IO.Compression.FileSystem'
[System.IO.Compression.ZipFile]::ExtractToDirectory('C:\temp\PSWindowsUpdate.zip', 'C:\temp\PSWindowsUpdate\')
```

Source:

http://www.sevenforums.com/tutorials/124198-user-profiles-create-move-during-windows-7-installation.html

Detailed instructions: 
http://www.sevenforums.com/attachments/tutorials/119213d1291161650-user-profiles-create-move-during-windows-7-installation-relocate-user-folders-during-windows-7-installation.pdf
