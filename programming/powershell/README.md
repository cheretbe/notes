Unsorted
* https://superuser.com/questions/468782/show-human-readable-file-sizes-in-the-default-powershell-ls-command/468907#468907

## Table of Contents
* [Useful Interactive Commands](#useful-interactive-commands)
* [Code Snippets](#code-snippets)
* [Remoting](#remoting)
* [Installation](#installation)
* [Remoting](./remoting.md)

## Useful Interactive Commands
```powershell
# System uptime
Get-CimInstance -ClassName Win32_OperatingSystem | Select LastBootUpTime
(get-date) – (gcim Win32_OperatingSystem).LastBootUpTime

# Physical disks info
Get-PhysicalDisk

# Logical disks info
Get-WmiObject Win32_LogicalDisk | ?{$_.DriveType -eq 3}
Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType = 3"

# List partitions
Get-WmiObject -Class Win32_Volume | 
  Select DriveLetter, Label,
    @{Label="Capacity (GB)";Expression={[math]::round($_.Capacity / 1GB, 2)}},
    @{Label="FreeSpace (GB)";Expression={[math]::round($_.Freespace / 1GB, 2)}},
    @{Label="Type";Expression={@{0="Unknown"; 1="No Root"; 2="Removable"; 3="Local"; 4="Network"; 5="CD"; 6="RAM Disk"}[[int]$_.DriveType]}},
    DeviceID |
  Format-Table -AutoSize
  
# List partitions similar to "lsblk" in linux
# https://stackoverflow.com/questions/31088930/combine-get-disk-info-and-logicaldisk-info-in-powershell/31092004#31092004
# https://superuser.com/questions/1206250/list-full-partition-information-from-powershell-just-like-from-disk-management
# https://vallentin.dev/2016/11/29/pretty-print-tree
Get-WmiObject Win32_DiskDrive | ForEach-Object {
  $drive = $_
  Write-Host ("$($drive.DeviceID): $($drive.Caption)")
  Get-Partition | Where-Object { $_.DiskNumber -eq $drive.Index } | ForEach-Object {
    $partition = $_
    Get-Volume | Where-Object { $partition.AccessPaths -contains $_.Path } | ForEach-Object {
      Write-Output ("   {0} - {1} {2} {3}GB; type: {4}; filesystem: {5}" -f $partition.PartitionNumber,
        $(if ($_.DriveLetter) { ($_.DriveLetter + ":") } else { "  " }),
        $_.FileSystemLabel,
        [math]::round($_.Size / 1GB, 2), $_.DriveType, $_.FileSystemType
      )
    }
  }
}

# Disk usage similar to "df -h" in Linux
Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType = 3" |
  Select-Object DeviceId, VolumeName,
     @{Name="Size (GB)";Expression={[math]::round($_.size / 1GB, 2)}},
     @{Name="Used (GB)";Expression={[math]::round(($_.size - $_.FreeSpace) / 1GB, 2)}},
     @{Name="Free (GB)";Expression={[math]::round($_.FreeSpace / 1GB, 2)}},
     @{Name="Use (%)";Expression={[math]::round(($_.size - $_.FreeSpace) * 100 / $_.size, 1)}} |
  Format-Table -AutoSize
```

## Code Snippets

```batch
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "%~dp0%~n0.ps1" %*

powershell.exe "Invoke-RestMethod https://freegeoip.app/json; Write-Host "Press any key..."; $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown') | Out-Null"
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
# [!] For PS 3.0+ use the following automatic variable:
$PSScriptRoot
```

```powershell
# Get domain user info
Add-Type -AssemblyName System.DirectoryServices.AccountManagement
[System.DirectoryServices.AccountManagement.UserPrincipal]::Current.EmailAddress

Set-ExecutionPolicy Bypass -Scope Process; iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/cheretbe/vagrant-files/develop/windows/provision/chocolatey.ps1'))

(
  New-Object -TypeName "Security.Principal.WindowsPrincipal" -ArgumentList ([Security.Principal.WindowsIdentity]::GetCurrent())
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
# or
(
  [Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent())
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

&"cmd.exe" @("/c", "ver")
Write-Host ("ERRORLEVEL: {0}" -f $LASTEXITCODE)

$processObj = Start-Process -FilePath "wusa.exe" -ArgumentList @($hotfixFileName, "/quiet", "/norestart") -Wait -PassThru
# Non-zero return code means error, except for the code 3010 (reboot is needed)
if (-not(($processObj.ExitCode -eq 0) -or ($processObj.ExitCode -eq 3010)))
  { Throw ("wusa.exe call failed: exit code {0}" -f $processObj.ExitCode) }

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

# [System.Text.Encoding], ASCII, Unicode, UTF-8, UTF-16
# Ansi -> OEM
# https://github.com/cheretbe/notes/blob/master/encodings.md#powershell

$zero = 0
try {
  1 / $zero
} catch {
  $_ | Add-Member NoteProperty writeErrorStream $TRUE -PassThru
  # Add-Member -MemberType ([System.Management.Automation.PSMemberTypes]::NoteProperty) -Name "writeErrorStream" -Value $TRUE -PassThru
  # Won't work in PS 2.0
  # $_ | Add-Member -NotePropertyName "writeErrorStream" -NotePropertyValue $TRUE -PassThru
}

# File redirection
. {
  Write-Output "Directory list:"
  Get-ChildItem "C:\"
} *>&1 | Tee-Object -Append -FilePath "test.log"

function Dummy {
[CmdletBinding()]
param(
  [Parameter(Mandatory=$TRUE,ValueFromPipeline=$TRUE)][string]$strParam,
  [switch]$switchParam,
  [string[]]$arrayOfStringsParam
)
  Begin {}
  # We need this because of a pipeline parameter
  Process {
    $switchParam.IsPresent
    # Pass through the switch to another cmdlet
    OtherDummy -switchParam:($switchParam.IsPresent)
  }
  End {}
}

# Passing variable by reference
function Test {
[CmdletBinding()]
param(
  [ref]$byRefParam
)
  # [!!!] Note .Value usage, not $byRefParam itself
  $byRefParam.Value = $TRUE
}

$byRefTest = $FALSE
Test -byRefParam ([ref]$byRefTest)
Write-Host ("byRefTest: {0}" -f $byRefTest)

# Add custom enum type
# PS 5.0+
enum MyEnum { aaa; bbb; ccc }
# Earlier versions
try {
  [void][MyEnum]
} catch {
  Add-Type -TypeDefinition "public enum MyEnum { aaa, bbb, ccc }"
}

Write-Host ((Get-ChildItem "c:\")[0] | Format-List * -Force | Out-String) -ForegroundColor Cyan

Join-Path -Path "dir" -ChildPath "subdir"
[system.io.path]::Combine("dir", "subdir")
[system.io.path]::Combine("dir", "subdir1", "subdir2", "subdir3", "subdir4")

Write-Host ([System.Environment]::ExpandEnvironmentVariables("%USERPROFILE%\Desktop"))
Write-Host ${Env:ProgramFiles(x86)}
$cpuArch = if (${Env:ProgramFiles(x86)}) { "x64" } else { "x86" }

if ([environment]::OSVersion.Version -ge ([version]"10.0"))
  { Write-Host "Windows 10+" }

# https://ss64.com/ps/syntax-f-operator.html
# Format examples
# parameter 0: round float to 3 decimal places after the point
# parameter 1: 4-digit integer (padded with leading zeroes)
("{0:n3} {1:d4}" -f 3.141592, 5)
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
$color = (Get-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "ImageColor" -ErrorAction SilentlyContinue).ImageColor
# Powershell 2.0 (Win7) has a bug: it returns DWORD values as int32, not uint32. This can cause an integer
# overflow for values like 0xC4FFFFFF
# The workaround is to compare values as hex strings:
$color.ToString("X") -eq (0xC4FFFFFF).ToString("X")
New-ItemProperty -Path "HKCU:\Console" -Name "FaceName" -Value "Consolas" -PropertyType ([Microsoft.Win32.RegistryValueKind]::String) -Force | Out-Null
New-Item 'HKCU:\Software\Policies\Microsoft\Windows\EdgeUI' -Force | New-ItemProperty # ... (no -Path)

Get-Date -Format "dd.MM.yyyy HH:mm:ss"
# ISO 8601 format
[DateTime]"1993-11-15T00:12:44"
[DateTime]::ParseExact("12 07 2012 18 02", "HH mm yyyy dd MM", $NULL)
[DateTime]::ParseExact("12 07 2012 18 02", "HH mm yyyy dd MM", [System.Globalization.CultureInfo]::InvariantCulture)

# http://msdn.microsoft.com/en-us/library/system.xml.xmlelement.aspx
# http://msdn.microsoft.com/en-us/library/system.xml.xmldocument.aspx
$xmlDoc = New-Object System.Xml.XmlDocument
# (?) does the following work?
#$xmlDoc = [System.Xml.XmlDocument]::new()

$rootNode = $xmlDoc.AppendChild($xmlDoc.CreateElement("root"))
# $xmlDoc.Load("test.xml")
# $rootNode = $xmlDoc.DocumentElement

# XPath examples
$nodeName = $xmlDoc.DocumentElement.SelectSingleNode('Directory[@Name="DirName"]/File[@Name="FileName"]').LocalName

$childNode = $rootNode.AppendChild($rootNode.OwnerDocument.CreateElement("Child"))
$childNode.InnerText = "child node value"
# or
$rootNode.AppendChild($rootNode.OwnerDocument.CreateElement("Child")).InnerText = "child node value"

#$attr = $childNode.OwnerDocument.CreateAttribute("AtrrName")
#$attr.Value = "AttrValue"
#$childNode.SetAttributeNode($attr) | Out-Null
$childNode.SetAttribute("AttrName", "AttrValue")
$xmlDoc.Save("c:\temp\test.xml")

# Reading key input
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown"):
# Alternative
[console]::ReadKey($TRUE)
# Or better yet? (review)
# http://stackoverflow.com/a/22362868

# https://docs.microsoft.com/en-us/dotnet/api/system.management.automation.host.pshostuserinterface.promptforchoice?view=powershellsdk-1.1.0
# Short version (no help). Use -1 for defaultChoice to not use a default choice
$host.ui.PromptForChoice("The Choice", "What is you selection?", @("&Yes", "&No"), 0)
# Long version with help
$options = [System.Management.Automation.Host.ChoiceDescription[]](
  (New-Object System.Management.Automation.Host.ChoiceDescription "&Yes", "Yes option description"),
  (New-Object System.Management.Automation.Host.ChoiceDescription "&No", "No option description")
)
$host.ui.PromptForChoice("The Choice", "What is you selection?", $options, 0)
      
# WMI Reference: http://www.powertheshell.com/reference/wmireference/
$ComputerSystemInfo = Get-WmiObject -Class Win32_ComputerSystem
# for a Virtualbox VM:
# $ComputerSystemInfo.Manufacturer: innotek GmbH
# $ComputerSystemInfo.Model       : VirtualBox
# for a KVM/QEMU VM:
# $ComputerSystemInfo.Manufacturer: QEMU
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
*.bat    text  eol=crlf

# Denote all files that are truly binary and should not be mergeable.
*.dll binary
*.exe binary
```

### Installation
  Check installed .NET versions: http://www.powershelladmin.com/wiki/Script_for_finding_which_dot_net_versions_are_installed_on_remote_workstations
  * Powershell 5.1
    * 1) .NET Framework 4.5.2: https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe
    ~~* 2) https://docs.microsoft.com/en-us/powershell/wmf/5.1/install-configure~~
    * 2) https://docs.microsoft.com/en-us/powershell/scripting/wmf/setup/install-configure?view=powershell-6
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
  * Powershell 4.0
    * 1) .NET Framework 4.5.2: https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe
    * 2) Windows Management Framework 4.0
      * Win7/2008R2
        * x86: https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows6.1-KB2819745-x86-MultiPkg.msu
        * x64: https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows6.1-KB2819745-x64-MultiPkg.msu
      * Win2012 (Win8 needs upgrade to 8.1)
        * x64: https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows8-RT-KB2799888-x64.msu

