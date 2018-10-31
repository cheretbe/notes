Command-line parameters:
* `-TestName` (Alias: Name). Example: `pester.bat -Name "StartsWith*"`
* `-Tag` (Alias: Tags). Example: `pester.bat -Tag "MyTag"`
* https://github.com/pester/Pester/wiki/Invoke-Pester


```powershell
"Actual value" | Should -Be "actual value"
"Actual value" | Should -BeExactly "Actual value"
6 | Should -Not -Be 5
```
* https://github.com/pester/Pester/wiki/Should

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

Assert-MockCalled Get-Thing -Exactly 1 -Scope It
Assert-MockCalled Get-Thing -Exactly 1 -Scope It -ParameterFilter { $InputObject -eq "dummy" }

$pathOne = "TestDrive:\somefile.txt"
$pathTwo = Join-Path $TestDrive "somefile.txt"
# $TestDrive holds the actual filesystem path
# Convert-Path "TestDrive:\"


$originalOSVerObj = $aoOSVersion
$aoOSVersion = $originalOSVerObj.PSObject.Copy()
$aoOSVersion.versionShort = "6.3"
# Usage
$aoOSVersion = $originalOSVerObj
```
