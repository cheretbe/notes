Command-line parameters:
* `-TestName` (Alias: Name). Example: `pester.bat -Name "StartsWith*"`
* `-Tag` (Alias: Tags). Example: `pester.bat -Tag "MyTag"`
* https://github.com/pester/Pester/wiki/Invoke-Pester


```powershell
Mock Get-Service { [pscustomobject]@{ "StartType" = ([System.ServiceProcess.ServiceStartMode]::Manual) }
{ throw [System.IO.FileNotFoundException] "file not found" } | Should -Throw -ExceptionType ([System.IO.FileNotFoundException])
```
