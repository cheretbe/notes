``` powershell
#[CmdletBinding(PositionalBinding=$FALSE)]
[CmdletBinding()]
param(
  [switch]$mySwitch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
```
