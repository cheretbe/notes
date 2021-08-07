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
   * version 2.0 (?): https://www.microsoft.com/en-us/download/details.aspx?id=25250
