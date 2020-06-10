* https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/sysprep-process-overview
* https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/how-configuration-passes-work

### Answer files
Answer files for Windows installer are prepared with `Windows System Image Manager`, which is a part of
Windows Assessment and Deployment Kit (Windows ADK).

* Links for download:
    * Windows 8.1 version: http://www.microsoft.com/en-us/download/details.aspx?id=39982
    * Windows 10 version: https://docs.microsoft.com/en-us/windows-hardware/get-started/adk-install

Only "Deployment Tools"  need to be installed in order to use WSIM.

Then run WSIM, select `Tools` > `Create Catalog`, point to
`sources\install.wim` file from windows installation DVD. This will create a catalog (.clg) file alongside the .wim file.
Only this file is needed later on for editing the answer file.

* https://docs.microsoft.com/en-us/windows-hardware/customize/desktop/unattend/components-b-unattend

### InstallFrom

* https://docs.microsoft.com/en-us/windows-hardware/customize/desktop/unattend/microsoft-windows-setup-imageinstall-dataimage-installfrom-metadata

`/unattend/settings[@pass='windowsPE']/component[@name='Microsoft-Windows-Setup']/ImageInstall/OSImage/InstallFrom/MetaData[@wcm:action="add"]` specifies a data
image in a Windows image (.wim) file.
Use the `MetaData\Key` and `MetaData\Value` settings together to select an image based on the index, the name, or the description of the data image.

Use the `DISM /Get-WimInfo` command to determine which images and editions are included:
```bat
dism.exe /Get-ImageInfo /ImageFile:c:\path\to\iso\contents\sources\install.wim
:: or
dism.exe /Get-WimInfo /WimFile:install.wim

:: When used with the /Index or /Name options, more detailed information
:: about the specified image is displayed
dism.exe /Get-WimInfo /WimFile:install.wim /Index:1
dism.exe /Get-ImageInfo /ImageFile:install.wim "/Name:Windows 10 Enterprise LTSC"
```
:warning: Gotcha: For Windows 10 LTSC 2019 both `/Get-WimInfo` and `/Get-ImageInfo` show image name
as `Windows 10 Enterprise LTSC`. But installer works only when `Windows 10 Enterprise LTSC 2019` is specified.
(WSIM `File` > `Select Windows Image` > `Select an Image` shows correct value).


Examples (`Key` and `Value` parameters **are case-sensitive**)
```xml
<!--Index-->
<MetaData wcm:action="add">
  <Key>/IMAGE/INDEX</Key>
  <Value>1</Value>
</MetaData>
<!--Name-->
<MetaData wcm:action="add">
  <Key>/IMAGE/NAME</Key>
  <Value>Windows 7 Enterprise</Value>
</MetaData>
<!--Description-->
<MetaData wcm:action="add">
  <Key>/IMAGE/DESCRIPTION</Key>
  <Value>Windows 7 Enterprise</Value>
</MetaData>
```

### Passwords
Passwords hashes are Base64-encoded representatios of the actual password concatenated with `Password` string (:warning: `AdministratorPassword` string is added for [AdministratorPassword](https://docs.microsoft.com/en-us/windows-hardware/customize/desktop/unattend/microsoft-windows-shell-setup-useraccounts-administratorpassword) parameter)

Powershell
```powershell
# ThePassw0rd ==> ThePassw0rdAdministratorPassword => VABoAGUAUABhAHMAcwB3ADAAcgBkAEEAZABtAGkAbgBpAHMAdAByAGEAdABvAHIAUABhAHMAcwB3AG8AcgBkAA==
[System.Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes("ThePassw0rdAdministratorPassword"))
# Convert back
[System.Text.Encoding]::Unicode.GetString([System.Convert]::Frombase64string("VABoAGUAUABhAHMAcwB3ADAAcgBkAEEAZABtAGkAbgBpAHMAdAByAGEAdABvAHIAUABhAHMAcwB3AG8AcgBkAA=="))
```
Python
```python
# By "unicode" MS mean UTF-16 LE
# Both b64encode and b64decode take and return bytes
import base64
base64.b64encode("ThePassw0rdAdministratorPassword".encode("utf-16le")).decode()
base64.b64decode("VABoAGUAUABhAHMAcwB3ADAAcgBkAEEAZABtAGkAbgBpAHMAdAByAGEAdABvAHIAUABhAHMAcwB3AG8AcgBkAA==").decode("utf-16le")
```
