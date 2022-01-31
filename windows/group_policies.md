```batch
:: See which group policies are applied to your PC and user account
rsop.msc

:: View all the policies applied to the user account you’re currently logged in with
gpresult /Scope User /v

:: View all the policies applied to your computer
gpresult /Scope Computer /v

gpedit.msc

gpupdate /force
```
* https://www.howtogeek.com/116184/how-to-see-which-group-policies-are-applied-to-your-pc-and-user-account/
* Group Policy Settings Reference for Windows and Windows Server: https://www.microsoft.com/en-us/download/details.aspx?id=25250
* https://superuser.com/questions/1192405/why-gpedit-and-the-corresponding-registry-entries-are-not-synchronized
* https://serverfault.com/questions/848388/how-to-edit-local-group-policy-with-a-script
* https://github.com/dlwyatt/PolicyFileEditor
   * https://web.archive.org/web/20181018000009/http://brandonpadgett.com/powershell/Local-gpo-powershell/
* https://docs.microsoft.com/en-us/archive/blogs/secguide/lgpo-exe-local-group-policy-object-utility-v1-0
   * version 3.0: https://www.microsoft.com/en-us/download/details.aspx?id=55319
* https://docs.microsoft.com/en-us/previous-versions/windows/desktop/Policy/registry-policy-file-format

Local group policy settings are stored in `Registry.pol` files located in `C:\Windows\system32\GroupPolicy`. These files overwrite the corresponding keys in the registry every time the system performs a group policy refresh. The editor **never actually reads the registry** to see what settings it contains.

A group policy refresh is triggered whenever one of the following events occurs:

* At a regularly scheduled refresh interval (every 90 minutes by default)
* A user logon or logoff event (user policy only)
* A computer reboot (computer policy only)
* A manually triggered refresh via gpupdate
* A policy refresh command issued by an admin from the domain controller (if the computer is domain-joined).

It's important to remember that if the computer is domain-joined, domain policies will be applied after the local group policy files are processed (meaning that some settings may get overwritten by domain policy). You will not be able to see domain policies in the local group policy editor.


```powershell
Install-Module -Name "nuget" -Force
Install-Module -Name "PolicyFileEditor" -Force

Set-ExecutionPolicy Bypass -Scope Process -Force
Import-Module PolicyFileEditor

$machineDir = "${ENV:SystemRoot}\system32\GroupPolicy\Machine\Registry.pol"
$userDir = "${ENV:SystemRoot}\system32\GroupPolicy\User\Registry.pol"

Get-PolicyFileEntry -Path $machineDir -All

Get-PolicyFileEntry -Path $machineDir -Key "SOFTWARE\Policies\Microsoft\Windows\System" -ValueName "EnableSmartScreen"

Set-PolicyFileEntry -Path $machineDir -Key "SOFTWARE\Policies\Microsoft\Windows\System" -ValueName "EnableSmartScreen" `
  -Type dword -Data 0 
```
