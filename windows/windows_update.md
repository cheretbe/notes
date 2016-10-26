Windows Update error code list: https://support.microsoft.com/en-us/kb/938205  
Update troubleshooter: https://support.microsoft.com/en-us/kb/971058  
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Detect

###Windows 8.1/2012R2
~~Update client (December 2015): https://support.microsoft.com/en-us/kb/3112336~~  
Update client (March 2016): https://support.microsoft.com/en-in/kb/3138615

###Windows 7/2008R2

1. KB3020369 (prerequisite for KB3125574): https://support.microsoft.com/en-gb/kb/3020369
2. KB3125574 Convenience rollup (download works in IE only): http://catalog.update.microsoft.com/v7/site/Search.aspx?q=KB3125574
3. KB3138612 Update Client: https://support.microsoft.com/en-us/kb/3138612
4. KB3172605 July 2016 update rollup: https://support.microsoft.com/en-us/kb/3172605

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
