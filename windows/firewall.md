```batch
:: View rule
netsh advfirewall firewall show rule name="_vagrant_WinRM-HTTP"
:: View all rules
netsh advfirewall firewall show rule name=all
:: Add rule
"%windir%\System32\netsh.exe" advfirewall firewall add rule name="_vagrant_WinRM-HTTP" dir=in localport=5985 protocol=TCP action=allow
```
