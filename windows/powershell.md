Unsorted
* https://superuser.com/questions/468782/show-human-readable-file-sizes-in-the-default-powershell-ls-command/468907#468907

## Table of Contents
* [Code Snippets](#code-snippets)
* [Remoting](#remoting)
* [Installation](#installation)

## Code Snippets

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

# [System.Text.Encoding]::ASCII
# [System.Text.Encoding]::Unicode (UTF-16 LE)
# [System.Text.Encoding]::UTF32 (UTF-32 LE)
# [System.Text.Encoding]::BigEndianUnicode (UTF-16 BE)
$oemEncoding = [System.Text.Encoding]::GetEncoding($Host.CurrentCulture.TextInfo.OEMCodePage)
$ansiEncoding = [System.Text.Encoding]::GetEncoding($Host.CurrentCulture.TextInfo.ANSICodePage)
# Powershell expects the output of a console command to be OEM-encoded and translates it to ANSI.
# But winrm.cmd is a wrapper around c:\windows\system32\winrm.vbs that already outputs ANSI text
& "winrm" | ForEach-Object { $ansiEncoding.GetString($oemEncoding.GetBytes($_)) }


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
### Remoting

```powershell
Enter-PSSession -UseSSL -ComputerName "host.domain.tld" -Credential "user" 2>&1
```

#### Unencrypted
```powershell
# On server
# -quiet: no prompts
# -force: enable even if public network is present
# winrm quickconfig [-quiet] [-force]
Enable-PSRemoting
# No prompts
Enable-PSRemoting -Force
# Enable even if public network is present
Enable-PSRemoting -SkipNetworkProfileCheck -Force
# Test if a computer can run remote commands
Test-WSMan [-ComputerName SRV1]

# On client
Set-Item "wsman:\localhost\Client\TrustedHosts" -Value "*" -Force
# Default WinRM port: 5985
# Enter-PSSession -ComputerName localhost -port 1111 -Credential vagrant
# This will prompt for a password
Enter-PSSession -ComputerName "hostname" -Credential "vagrant" 2>&1
# This will not
$pwd = ConvertTo-SecureString "vagrant" -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential @("vagrant", $pwd)
Enter-PSSession -ComputerName "hostname" -Credential $credential 2>&1
# Run scriptblock
Invoke-Command -ComputerName "hostname" -Credential $credential -ScriptBlock { & cmd /c set }
# Save/load credentials
$credential | Export-CliXml -Path "C:\My\Path\cred.xml"
$credential = Import-CliXml -Path "C:\My\Path\cred.xml"
# or
$credential.Password | ConvertFrom-SecureString | Out-File "C:\My\Path\pwd.txt"
$pwd = (Get-Content "C:\My\Path\pwd.txt" | ConvertTo-SecureString)
```

#### HTTP with a self-signed SSL certificate
* https://4sysops.com/archives/powershell-remoting-over-https-with-a-self-signed-ssl-certificate/

By default `New-SelfSignedCertificate` creates a certificate that is valid for one year. To create a certificate that lasts longer use `-NotAfter (Get-Date).AddYears(5)` parameter. The problem is that this parameter doesn't work on Win8.1/Win2012R2 (even with PS 5.1 installed):  https://social.technet.microsoft.com/Forums/windowsserver/en-US/cd5bba06-5931-42ee-afad-1e438b3df759/problem-generating-a-certificate-for-ldaps-using-newselfsignedcertificate-quota-parameter?forum=winserver8gen

The solution is to use openssl:

```shell
# EKU should contain serverAuth and this parameter can't be passed as a command-line option
# We create a temporary config file to add it
cp /usr/lib/ssl/openssl.cnf ./ext_config.cnf
```
Add the following to `ext_config.cnf`:
```
[myextensions]
extendedKeyUsage = serverAuth,clientAuth
```
```shell
# Create a self-signed certificate
openssl req \
       -newkey rsa:2048 -nodes -keyout domain.key \
       -x509 -days 3650 -out domain.crt \
       -extensions myextensions -config ext_config.cnf
# Take a private key (domain.key) and a certificate (domain.crt), and combine them into a PKCS12 file (domain.pfx):
openssl pkcs12 \
       -inkey domain.key \
       -in domain.crt \
       -export -out domain.pfx
```
Copy `domain.pfx` to a Windows machine
```powershell
# Import the certificate
Import-PfxCertificate -FilePath "c:\temp\domain.pfx" -CertStoreLocation "Cert:\LocalMachine\My" -Exportable
# View certificate list to find out the thumbprint
Get-ChildItem "Cert:\LocalMachine\My" | Format-List
# Delete a certificate (in case something went wrong)
Get-ChildItem "Cert:\LocalMachine\My" |
  Where-Object { $_.Thumbprint -eq '0000000000000000000000000000000000000000' } | Remove-Item
```
Everything is else should be done as described in the linked howto

### Installation
  Check installed .NET versions: http://www.powershelladmin.com/wiki/Script_for_finding_which_dot_net_versions_are_installed_on_remote_workstations
  * Powershell 5.1
    * 1) .NET Framework 4.5.2: https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe
    * 2) https://docs.microsoft.com/en-us/powershell/wmf/5.1/install-configure
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
