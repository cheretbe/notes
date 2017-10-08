```powershell
Set-ExecutionPolicy Bypass -Scope Process; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

* https://github.com/chocolatey/choco/wiki/How-To-Host-Feed

```bat
choco install MyPackage -source c:\MyDirectory [-version 1.2.3.4] [-f] [-y]
choco uninstall MyPackage [-y]
```
