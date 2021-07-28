* https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/export-or-import-default-application-associations
* https://docs.microsoft.com/ru-ru/archive/blogs/windowsinternals/windows-10-how-to-configure-file-associations-for-it-pros
* https://techcult.com/export-and-import-default-app-associations-in-windows-10/
* https://www.loginvsi.com/login-vsi-blog/login-vsi/518-fixing-default-file-type-associations-in-windows-10
* https://stackoverflow.com/questions/37018372/dism-import-defaultappassociations-runs-successfully-but-no-file-associations/38234773#38234773
* Summary
    * GPO con: doesn't really respect/keep users app associations, it resets them back to your GPO ones on each login. You could apply the GPO for a month & disable?
    * GPO con: only works for domain PC's, if you configure it on a local gpedit.msc it will simply not work
    * DISM pro: respects users app associations since it appears to only run once on new user setup (?)
  * DISM con: as noted above only works for new users. Crappy solution: delete user profile
       * ❓Try to create custom `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.ext\UserChoice` values with updated `Hash` parameter
       * https://stackoverflow.com/questions/17946282/whats-the-hash-in-hkcu-software-microsoft-windows-currentversion-explorer-filee
       * https://kolbi.cz/blog/2017/10/25/setuserfta-userchoice-hash-defeated-set-file-type-associations-per-user/
  * All DISM commands appear to work with `%SystemRoot%\System32\OEMDefaultAssociations.xml` file. Do they use anything else?
```batch
dism.exe /Online /Export-DefaultAppAssociations:"%UserProfile%\Desktop\DefaultAppAssociations.xml"
dism.exe /Online /Import-DefaultAppAssociations:"%UserProfile%\Desktop\DefaultAppAssociations.xml"
dism.exe /Online /Remove-DefaultAppAssociations
```
