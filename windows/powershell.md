```batch
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "%~dp0%~n0.ps1"
```

``` powershell
#[CmdletBinding(PositionalBinding=$FALSE)]
[CmdletBinding()]
param(
  [switch]$mySwitch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = [System.Management.Automation.ActionPreference]::Stop
$Host.PrivateData.VerboseForegroundColor = [ConsoleColor]::DarkCyan

$script:scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
```

```powershell
Set-ExecutionPolicy Bypass -Scope Process; iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/cheretbe/vagrant-files/develop/windows/provision/chocolatey.ps1'))

(
  New-Object -TypeName "Security.Principal.WindowsPrincipal" -ArgumentList ([Security.Principal.WindowsIdentity]::GetCurrent())
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

&"cmd.exe" @("/c", "ver")
Write-Host ("ERRORLEVEL: {0}" -f $LASTEXITCODE)

[enum]::GetValues([System.Management.Automation.PSMemberTypes])

# File output
# Write file using UTF-8 with no BOM
[System.IO.File]::WriteAllLines($filePath, $fileContent)
# Append to a file (UTF16 with BOM)
"new line" | Out-File -Append -FilePath $filePath
# Append to a file (current ANSI encoding with no BOM)
Add-Content -Path $filePath -Value "new line"
# Append to a file with Linux-style line endings
[System.IO.File]::AppendAllText($filePath, "new line`n")

# Add line to a file if not already present
if ($NULL -eq (Get-Content $filePath | Where-Object { $_.Contains($newText) })) {
  Add-Content $filePath $newText
} #if


$zero = 0
try {
  1 / $zero
} catch {
  $_ | Add-Member NoteProperty writeErrorStream $TRUE -PassThru
  # Add-Member -MemberType ([System.Management.Automation.PSMemberTypes]::NoteProperty) -Name "writeErrorStream" -Value $TRUE -PassThru
  # Won't work in PS 2.0
  # $_ | Add-Member -NotePropertyName "writeErrorStream" -NotePropertyValue $TRUE -PassThru
}

function Dummy {
[CmdletBinding()]
param(
  [switch]$switchParam,
  [string[]]$arrayOfStringsParam
)
  $switchParam.IsPresent
  # Pass through the switch to another cmdlet
  OtherDummy -switchParam:($switchParam.IsPresent)
}

Write-Host ((Get-ChildItem "c:\")[0] | Format-List * -Force | Out-String) -ForegroundColor Cyan

Write-Host ${Env:ProgramFiles(x86)}
$cpuArch = if (${Env:ProgramFiles(x86)}) { "x64" } else { "x86" }

if ([environment]::OSVersion.Version -ge ([version]"10.0"))
  { Write-Host "Windows 10+" }

# Escape curly braces when used with -f operator
Write-Host ("{{ {0} }}" -f "test")

Join-Path -Path $FilePath -ChildPath $FileName

if (Test-Path -Path $DirPath) {
  Remove-Item -Path $DirPath -Recurse -Force
}

# Creates parent directories as needed by default
# -Force causes New-Item not to fail if the directory already exists
# ItemType is a string
New-Item -ItemType "Directory" -Path $dir_to_create -Force | Out-Null 

[enum]::GetValues([Microsoft.Win32.RegistryValueKind])
New-ItemProperty -Path "HKCU:\Console" -Name "FaceName" -Value "Consolas" -PropertyType ([Microsoft.Win32.RegistryValueKind]::String) -Force

Get-Date -Format "dd.MM.yyyy HH:mm:ss"

# Reading key input
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown"):
# Alternative
[console]::ReadKey($TRUE)
# Or better yet? (review)
# http://stackoverflow.com/a/22362868

# WMI Reference: http://www.powertheshell.com/reference/wmireference/
$ComputerSystemInfo = Get-WmiObject -Class Win32_ComputerSystem
# for a Virtualbox VM:
# $ComputerSystemInfo.Manufacturer: innotek GmbH
# $ComputerSystemInfo.Model       : VirtualBox
```

` .gitattributes` file
```
# Set default behaviour, in case users don't have core.autocrlf set.
* text=auto

# Explicitly declare text files we want to always be normalized and converted
# to native line endings on checkout.
*.md            text
*.gitattributes text

# Declare files that will always have CRLF line endings on checkout.
*.ps1    text  eol=crlf
*.psm1   text  eol=crlf
*.psd1   text  eol=crlf
*.psc1   text  eol=crlf
*.ps1xml text  eol=crlf
*.clixml text  eol=crlf
*.xml    text  eol=crlf
*.txt    text  eol=crlf

# Denote all files that are truly binary and should not be mergeable.
*.dll binary
*.exe binary
```

### Installation
  Check installed .NET versions: http://www.powershelladmin.com/wiki/Script_for_finding_which_dot_net_versions_are_installed_on_remote_workstations
  * Powershell 4.0
    * 1) .NET Framework 4.5.2: https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe
    * 2) Windows Management Framework 4.0
      * Win7/2008R2
        * x86: https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows6.1-KB2819745-x86-MultiPkg.msu
        * x64: https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows6.1-KB2819745-x64-MultiPkg.msu
      * Win2012 (Win8 needs upgrade to 8.1)
        * x64: https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows8-RT-KB2799888-x64.msu
  * Powershell 5.0
    * 1) .NET Framework 4.5.2: https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe
    * 2) Windows Management Framework 5.0
      * Win7/2008R2
        * x86: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/Win7-KB3134760-x86.msu
        * x64: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/Win7AndW2K8R2-KB3134760-x64.msu
      * Win2012 (Win8 needs upgrade to 8.1)
        * x64: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/W2K12-KB3134759-x64.msu
      * Win8.1/2012R2
        * x86: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/Win8.1-KB3134758-x86.msu
        * x64: https://download.microsoft.com/download/2/C/6/2C6E1B4A-EBE5-48A6-B225-2D2058A9CEFB/Win8.1AndW2K12R2-KB3134758-x64.msu
