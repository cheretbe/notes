```batch
"%windir%\System32\netsh.exe" advfirewall firewall add rule name="_vagrant_WinRM-HTTP" dir=in localport=5985 protocol=TCP action=allow
```
