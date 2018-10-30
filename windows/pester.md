Command-line parameters:
* `-TestName` (Alias: Name). Example: `pester.bat -Name "StartsWith*"`
* `-Tag` (Alias: Tags). Example: `pester.bat -Tag "MyTag"`
* https://github.com/pester/Pester/wiki/Invoke-Pester


```powershell
mock Get-Thing {
  [PSCustomObject]@{
    Property = "Value"
    SubObject = [PSCustomObject]@{
      SubProperty = "Value1"
    }
  }
}
Mock Get-Service { [PSCustomObject]@{ "StartType" = ([System.ServiceProcess.ServiceStartMode]::Manual) }
{ throw [System.IO.FileNotFoundException] "file not found" } | Should -Throw -ExceptionType ([System.IO.FileNotFoundException])

$originalOSVerObj = $aoOSVersion
$aoOSVersion = $originalOSVerObj.PSObject.Copy()
$aoOSVersion.versionShort = "6.3"
# Usage
$aoOSVersion = $originalOSVerObj
```
