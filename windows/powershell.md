### Installation
  Check installed .NET versions: http://www.powershelladmin.com/wiki/Script_for_finding_which_dot_net_versions_are_installed_on_remote_workstations
  * Powershell 4.0
    * 1) .NET Framework 4.5.2: https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe
    * 2) Windows Management Framework 4.0
      * Win7/2008R2
        * x86: https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows6.1-KB2819745-x86-MultiPkg.msu
        * x64: https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows6.1-KB2819745-x64-MultiPkg.msu
      * Win2012 (Win8 needs upgrade to 8.1)
        * x64: https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows8-RT-KB2799888-x64.msu
  * Powershell 5.0
    * 1) .NET Framework 4.5.2: https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe
    * 2) Windows Management Framework 5.0
      * Win7/2008R2
        * x86: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/Win7-KB3134760-x86.msu
        * x64: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/Win7AndW2K8R2-KB3134760-x64.msu
      * Win2012 (Win8 needs upgrade to 8.1)
        * x64: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/W2K12-KB3134759-x64.msu
      * Win8.1/2012R2
        * x86: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/Win8.1-KB3134758-x86.msu
        * x64: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/Win8.1AndW2K12R2-KB3134758-x64.msu

```powershell
Write-Host ((Get-ChildItem "c:\")[0] | Format-List * -Force | Out-String) -ForegroundColor Cyan
```
