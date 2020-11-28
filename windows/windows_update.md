* Windows Update error code list: https://support.microsoft.com/en-us/kb/938205  
* Update troubleshooter: https://support.microsoft.com/en-us/kb/971058  
* Windows Update Catalog: https://www.catalog.update.microsoft.com/Home.aspx  
* https://i.imgur.com/MBRIMMX.png

### Completely disabling Windows Update

```bat
:: Windows Update
sc.exe config wuauserv start= disabled
:: Update Orchestrator Service
sc.exe config UsoSvc start= disabled
```
Check scheduled tasks under `\Microsoft\Windows\WindowsUpdate` and `\Microsoft\Windows\UpdateOrchestrator`

```powershell
# Run command prompt as SYSTEM account
 Start-Process -FilePath cmd.exe -Verb Runas -ArgumentList '/k \\live.sysinternals.com\tools\PsExec64.exe -i -s cmd.exe'
# Then run Task Scheduler console 
%windir%\system32\taskschd.msc /s
```

---
* https://www.dedoimedo.com/computers/windows-10-updates-improvements-control.html
* https://www.reddit.com/r/Windows10/comments/aavqpm/after_6_months_of_testing_this_in_my_company_i/

### PSWindowsUpdate
```powershell
Install-PackageProvider -Name NuGet -Force
Install-Module -Name PSWindowsUpdate -Force

get-command -Module PSWindowsUpdate
# [!] Set execution policy to "unrestricted" to view help
get-help Get-WindowsUpdate

Set-ExecutionPolicy Unrestricted -Force -Scope Process
$progressPreference = "SilentlyContinue"
Set-Service -Name "wuauserv" -StartupType Manual
Get-WindowsUpdate -Install -AcceptAll -IgnoreReboot
Get-WURebootStatus -Silent


Add-WUServiceManager -MicrosoftUpdate -Confirm:$FALSE
Get-WindowsUpdate -MicrosoftUpdate -Install -AcceptAll -IgnoreReboot
```
* https://www.powershellgallery.com/packages/PSWindowsUpdate/
* http://woshub.com/pswindowsupdate-module/

View last update times
```cmd
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Detect" /v LastSuccessTime
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Download" /v LastSuccessTime
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Install" /v LastSuccessTime
```

Turn on Microsoft Update
```powershell
# Powershell
(New-Object -ComObject Microsoft.Update.ServiceManager -Strict).AddService2("7971f918-a847-4430-9279-4a52d1efe18d", 7, "") | Out-Null
```

###Windows 8.1/2012R2

1. KB2919442 (Prerequisite for KB2919355) March 2014 servicing stack update for Windows 8.1/2012R2 https://support.microsoft.com/en-us/kb/2919442
  * x86: https://download.microsoft.com/download/9/D/A/9DA6C939-9E65-4681-BBBE-A8F73A5C116F/Windows8.1-KB2919442-x86.msu
  * x64: https://download.microsoft.com/download/C/F/8/CF821C31-38C7-4C5C-89BB-B283059269AF/Windows8.1-KB2919442-x64.msu
2. KB2919355 (prerequisite for KB3138615) April 2014 update for Windows 8.1/2012R2 https://support.microsoft.com/en-us/kb/2919355
  * 2-1 Clearcompressionflag.exe tool
    * x86: http://download.microsoft.com/download/4/E/C/4EC66C83-1E15-43FD-B591-63FB7A1A5C04/clearcompressionflag.exe
    * x64: http://download.microsoft.com/download/D/B/1/DB1F29FC-316D-481E-B435-1654BA185DCF/clearcompressionflag.exe
  * 2-2 KB2919355
    * x86: https://download.microsoft.com/download/4/E/C/4EC66C83-1E15-43FD-B591-63FB7A1A5C04/Windows8.1-KB2919355-x86.msu
    * x64: https://download.microsoft.com/download/D/B/1/DB1F29FC-316D-481E-B435-1654BA185DCF/Windows8.1-KB2919355-x64.msu
  * 2-3 KB2932046
    * x86: https://download.microsoft.com/download/4/E/C/4EC66C83-1E15-43FD-B591-63FB7A1A5C04/Windows8.1-KB2932046-x86.msu
    * x64: https://download.microsoft.com/download/D/B/1/DB1F29FC-316D-481E-B435-1654BA185DCF/Windows8.1-KB2932046-x64.msu
  * 2-4 KB2959977
    * x86: https://download.microsoft.com/download/4/E/C/4EC66C83-1E15-43FD-B591-63FB7A1A5C04/Windows8.1-KB2959977-x86.msu
    * x64: https://download.microsoft.com/download/D/B/1/DB1F29FC-316D-481E-B435-1654BA185DCF/Windows8.1-KB2959977-x64.msu
  * 2-5 KB2937592
    * x86: https://download.microsoft.com/download/4/E/C/4EC66C83-1E15-43FD-B591-63FB7A1A5C04/Windows8.1-KB2937592-x86.msu
    * x64: https://download.microsoft.com/download/D/B/1/DB1F29FC-316D-481E-B435-1654BA185DCF/Windows8.1-KB2937592-x64.msu
  * 2-6 KB2938439
    * x86: https://download.microsoft.com/download/4/E/C/4EC66C83-1E15-43FD-B591-63FB7A1A5C04/Windows8.1-KB2938439-x86.msu
    * x64: https://download.microsoft.com/download/D/B/1/DB1F29FC-316D-481E-B435-1654BA185DCF/Windows8.1-KB2938439-x64.msu
  * 2-7 KB2934018
    * x86: https://download.microsoft.com/download/4/E/C/4EC66C83-1E15-43FD-B591-63FB7A1A5C04/Windows8.1-KB2934018-x86.msu
    * x64: https://download.microsoft.com/download/D/B/1/DB1F29FC-316D-481E-B435-1654BA185DCF/Windows8.1-KB2934018-x64.msu
3. KB3138615 Update client for Windows 8.1/2012R2 (March 2016): https://support.microsoft.com/en-us/kb/3138615
  * x86: https://download.microsoft.com/download/9/6/4/964EE585-03DC-441A-AA99-6A39BA731869/Windows8.1-KB3138615-x86.msu
  * x64: https://download.microsoft.com/download/8/8/A/88AFE5D4-0021-4384-9D64-5411257CCC5B/Windows8.1-KB3138615-x64.msu

###Windows 7/2008R2

1. KB3020369 (prerequisite for KB3125574): https://support.microsoft.com/en-gb/kb/3020369
  * x86: https://download.microsoft.com/download/C/0/8/C0823F43-BFE9-4147-9B0A-35769CBBE6B0/Windows6.1-KB3020369-x86.msu
  * x64: https://download.microsoft.com/download/5/D/0/5D0821EB-A92D-4CA2-9020-EC41D56B074F/Windows6.1-KB3020369-x64.msu
2. KB3125574 Convenience rollup
  * https://support.microsoft.com/en-us/kb/3125574
  * http://catalog.update.microsoft.com/v7/site/Search.aspx?q=KB3125574
    * x86: http://download.windowsupdate.com/d/msdownload/update/software/updt/2016/05/windows6.1-kb3125574-v4-x86_ba1ff5537312561795cc04db0b02fbb0a74b2cbd.msu
    * x64: http://download.windowsupdate.com/d/msdownload/update/software/updt/2016/05/windows6.1-kb3125574-v4-x64_2dafb1d203c8964239af3048b5dd4b1264cd93b9.msu
3. KB3138612 Update Client for Windows 7/2008R2 (March 2016): https://support.microsoft.com/en-us/kb/3138612
  * x86: https://download.microsoft.com/download/E/4/7/E47FB37E-7443-4047-91F7-16DDDCF2955C/Windows6.1-KB3138612-x86.msu
  * x64: https://download.microsoft.com/download/B/7/C/B7CD3A70-1EA7-486A-9585-F6814663F1A9/Windows6.1-KB3138612-x64.msu
4. KB3172605 July 2016 update rollup: https://support.microsoft.com/en-us/kb/3172605
 * x86: https://download.microsoft.com/download/C/D/5/CD5DE7B2-E857-4BD4-AA9C-6B30C3E1735A/Windows6.1-KB3172605-x86.msu
 * x64: https://download.microsoft.com/download/5/6/0/560504D4-F91A-4DEB-867F-C713F7821374/Windows6.1-KB3172605-x64.msu

### Windows 2012

KB2937636 Windows Update Agent for Windows 8 and Windows Server 2012: https://support.microsoft.com/en-us/kb/2887535

x64: https://download.microsoft.com/download/C/4/F/C4F803A8-D91E-435E-90BF-5BCB019A4010/Windows8-RT-KB2937636-x64.msu

After that the rest of updates can be installed normally

###Registering WU DLLs

![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) Note `System32\Catroot2` and `SoftwareDistribution` rename
```
net stop wuauserv
net stop bits
net stop cryptsvc

ren %systemroot%\System32\Catroot2 Catroot2.old
ren %systemroot%\SoftwareDistribution SoftwareDistribution.old

regsvr32 c:\windows\system32\vbscript.dll /s
regsvr32 c:\windows\system32\mshtml.dll /s
regsvr32 c:\windows\system32\msjava.dll /s
regsvr32 c:\windows\system32\jscript.dll /s
regsvr32 c:\windows\system32\msxml.dll /s
regsvr32 c:\windows\system32\actxprxy.dll /s
regsvr32 c:\windows\system32\shdocvw.dll /s
regsvr32 wuapi.dll /s
regsvr32 wuaueng1.dll /s
regsvr32 wuaueng.dll /s
regsvr32 wucltui.dll /s
regsvr32 wups2.dll /s
regsvr32 wups.dll /s
regsvr32 wuweb.dll /s
regsvr32 Softpub.dll /s
regsvr32 Mssip32.dll /s
regsvr32 Initpki.dll /s
regsvr32 softpub.dll /s
regsvr32 wintrust.dll /s
regsvr32 initpki.dll /s
regsvr32 dssenh.dll /s
regsvr32 rsaenh.dll /s
regsvr32 gpkcsp.dll /s
regsvr32 sccbase.dll /s
regsvr32 slbcsp.dll /s
regsvr32 cryptdlg.dll /s
regsvr32 Urlmon.dll /s
regsvr32 Shdocvw.dll /s
regsvr32 Msjava.dll /s
regsvr32 Actxprxy.dll /s
regsvr32 Oleaut32.dll /s
regsvr32 Mshtml.dll /s
regsvr32 msxml.dll /s
regsvr32 msxml2.dll /s
regsvr32 msxml3.dll /s
regsvr32 Browseui.dll /s
regsvr32 shell32.dll /s
regsvr32 wuapi.dll /s
regsvr32 wuaueng.dll /s
regsvr32 wuaueng1.dll /s
regsvr32 wucltui.dll /s
regsvr32 wups.dll /s
regsvr32 wuweb.dll /s
regsvr32 jscript.dll /s
regsvr32 atl.dll /s
regsvr32 Mssip32.dll /s

net start wuauserv
net start bits
net start cryptsvc

PAUSE
```
