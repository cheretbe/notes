`/unattend/settings[@pass='windowsPE']/component[@name='Microsoft-Windows-Setup']/ImageInstall/OSImage/InstallFrom/MetaData[@wcm:action="add"]` specifies a data
image in a Windows image (.wim) file.
Use the `MetaData\Key` and `MetaData\Value` settings together to select an image based on the index, the name, or the description of the data image.

Use the `DISM /Get-WimInfo` command to determine which images and editions are included:
```bat
dism.exe /Get-ImageInfo /ImageFile:c:\path\to\iso\contents\install.wim
:: or
dism.exe /Get-WimInfo /WimFile:install.wim

:: When used with the /Index or /Name options, more detailed information
:: about the specified image is displayed
dism.exe /Get-WimInfo /WimFile:install.wim /Index:1
dism.exe /Get-ImageInfo /ImageFile:install.wim "/Name:Windows 10 Enterprise LTSC"
```
Examples (`Key` and `Value` paramaters **are case-sensitive**)
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
