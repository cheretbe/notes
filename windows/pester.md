```powershell
Mock Get-Service { [pscustomobject]@{ "StartType" = ([System.ServiceProcess.ServiceStartMode]::Manual }
```
