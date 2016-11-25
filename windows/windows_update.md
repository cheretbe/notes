Windows Update error code list: https://support.microsoft.com/en-us/kb/938205  
Update troubleshooter: https://support.microsoft.com/en-us/kb/971058  
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Detect

###Windows 8.1/2012R2
~~Update client (December 2015): https://support.microsoft.com/en-us/kb/3112336~~
* https://download.microsoft.com/download/C/6/0/C60E8D85-FD51-4B27-A78F-7F68093A1DCF/Windows8.1-KB3112336-x86.msu
* https://download.microsoft.com/download/0/6/5/06585DC5-F6E3-4DB8-B11C-DD8CCF867DF3/Windows8.1-KB3112336-x64.msu


1. (Prerequisite) March 2014 servicing stack update for Windows 8.1 and Windows Server 2012 R2  https://support.microsoft.com/en-us/kb/2919442
2. Clearcompressionflag.exe tool
  * x86: http://download.microsoft.com/download/4/E/C/4EC66C83-1E15-43FD-B591-63FB7A1A5C04/clearcompressionflag.exe
  * x64: http://download.microsoft.com/download/D/B/1/DB1F29FC-316D-481E-B435-1654BA185DCF/clearcompressionflag.exe
3. (Prerequisite) Windows RT 8.1, Windows 8.1, and Windows Server 2012 R2 update: April 2014 http://support.microsoft.com/kb/2919355
4. Update client (March 2016): https://support.microsoft.com/en-in/kb/3138615

###Windows 7/2008R2

1. KB3020369 (prerequisite for KB3125574): https://support.microsoft.com/en-gb/kb/3020369
  * x86: https://download.microsoft.com/download/C/0/8/C0823F43-BFE9-4147-9B0A-35769CBBE6B0/Windows6.1-KB3020369-x86.msu
  * x64: https://download.microsoft.com/download/5/D/0/5D0821EB-A92D-4CA2-9020-EC41D56B074F/Windows6.1-KB3020369-x64.msu
2. KB3125574 Convenience rollup
  * https://support.microsoft.com/en-us/kb/3125574
  * http://catalog.update.microsoft.com/v7/site/Search.aspx?q=KB3125574
    * x86: http://download.windowsupdate.com/d/msdownload/update/software/updt/2016/05/windows6.1-kb3125574-v4-x86_ba1ff5537312561795cc04db0b02fbb0a74b2cbd.msu
    * x64: http://download.windowsupdate.com/d/msdownload/update/software/updt/2016/05/windows6.1-kb3125574-v4-x64_2dafb1d203c8964239af3048b5dd4b1264cd93b9.msu
3. KB3138612 Update Client (March 2016): https://support.microsoft.com/en-us/kb/3138612
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
