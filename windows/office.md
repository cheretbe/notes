* https://4sysops.com/archives/install-only-selected-office-applications-using-the-office-deployment-tool/
* https://winitpro.ru/index.php/2019/09/04/razvertyvanie-office-2019-volume/
* :warning: https://winitpro.ru/index.php/2020/01/27/kak-vyborochno-ustanovit-prilozheniya-v-office/

```bat
reg add HKCU\SOFTWARE\Microsoft\Office\16.0\Common\Licensing /v EulasSetAccepted /t REG_SZ /d 0,16,28, /f
reg add HKCU\SOFTWARE\Microsoft\Office\16.0\Common\General /v ShownFirstRunOptin /t REG_DWORD /d 1 /f
```

```
REGEDIT4

[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Common]
"PrivacyNoticeShown"=dword:00000002

[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Common\PTWatson]
"PTWOptIn"=dword:00000000
"PTWReadyToSend"=dword:00000000
"PTWNextUpload"=dword:00000000
"PTWCount"=dword:00000000
"PTWExpire"=dword:00000000


[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Common\Research\Options]
"LastDeepRegistration"=dword:00005ec4
"DiscoveryNeedOptIn"=dword:00000001

[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Common\Security\FileValidation]
"DisableReporting"=dword:00000001

[HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Word\Security\FileBlock\OoxmlConverters]
"{A5C79653-FC73-46ee-AD3E-B64C01268DAA}"=dword:00000000

```
