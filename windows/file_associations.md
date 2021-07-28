* https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/export-or-import-default-application-associations
* https://docs.microsoft.com/ru-ru/archive/blogs/windowsinternals/windows-10-how-to-configure-file-associations-for-it-pros
* https://techcult.com/export-and-import-default-app-associations-in-windows-10/
* https://www.loginvsi.com/login-vsi-blog/login-vsi/518-fixing-default-file-type-associations-in-windows-10
* https://stackoverflow.com/questions/37018372/dism-import-defaultappassociations-runs-successfully-but-no-file-associations/38234773#38234773

```batch
dism.exe /Online /Export-DefaultAppAssociations:"%UserProfile%\Desktop\DefaultAppAssociations.xml"
dism.exe /Online /Import-DefaultAppAssociations:"%UserProfile%\Desktop\DefaultAppAssociations.xml"
dism.exe /Online /Remove-DefaultAppAssociations
```
