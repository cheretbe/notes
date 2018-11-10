* https://github.com/alphaleonis/AlphaFS
* https://github.com/alphaleonis/AlphaFS/wiki/PowerShell
---
```powershell
Import-Module (Join-Path -Path (Split-Path -Parent $MyInvocation.MyCommand.Path) -ChildPath "AlphaFS\lib\net40\AlphaFS.dll")
```
```powershell
# revision 1; 10.11.2018
try {
  [void][afDirEnumOptions]
} catch {
  Add-Type -TypeDefinition "public enum afDirEnumOptions { Files, Folders, FilesAndFolders }"
}

function afEnumerateFSEntryInfos {
[CmdletBinding()]
param(
  [Parameter(Mandatory=$TRUE,ValueFromPipeline=$TRUE)][string]$Path,
  [Alphaleonis.Win32.Filesystem.PathFormat]$PathFormat = [Alphaleonis.Win32.Filesystem.PathFormat]::FullPath,
  [afDirEnumOptions]$DirEnumOptions = [afDirEnumOptions]::FilesAndFolders,
  [switch]$SkipReparsePoints,
  [switch]$ContinueOnException,
  [switch]$Recursive
)
  Process {
    switch ($DirEnumOptions) {
      ([afDirEnumOptions]::Files)
        { $FullDirEnumOptions = [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::Files }
      ([afDirEnumOptions]::Folders)
        { $FullDirEnumOptions = [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::Folders }
      ([afDirEnumOptions]::FilesAndFolders)
        { $FullDirEnumOptions = [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::FilesAndFolders }
    } #switch
    if ($SkipReparsePoints.IsPresent)
      { $FullDirEnumOptions = $FullDirEnumOptions -bor [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::SkipReparsePoints}
    if ($ContinueOnException.IsPresent)
      { $FullDirEnumOptions = $FullDirEnumOptions -bor [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::ContinueOnException}
    if ($Recursive.IsPresent)
      { $FullDirEnumOptions = $FullDirEnumOptions -bor [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::Recursive}

    $Instance = ([Alphaleonis.Win32.Filesystem.Directory])
    $MethodParameters = @($Path, $FullDirEnumOptions, $PathFormat)
    [Collections.ArrayList]$Private:ParameterTypes = @{}
    foreach ($private:ParamType in $MethodParameters)
      { [void]$ParameterTypes.Add($ParamType.GetType()) }
    $private:Method = $Instance.GetMethod("EnumerateFileSystemEntryInfos",
      "Instance, Static, Public", $NULL, $ParameterTypes, $NULL)
    $Method = $Method.MakeGenericMethod(@(([Alphaleonis.Win32.Filesystem.FileSystemEntryInfo])))
    $Method.Invoke($Instance, $MethodParameters)
  } #Process
}
```

* `Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions`: `None` (do not use), `Files`, `Folders`, `FilesAndFolders`,
  `AsLongPath`, `SkipReparsePoints`, `ContinueOnException`, `Recursive`, `BasicSearch` (no short names), `LargeCache`
* `System.IO.SearchOption`: `AllDirectories`, `TopDirectoryOnly`

```powershell
$searchOptions = [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::Folders -bor `
  [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::SkipReparsePoints -bor `
  [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::Recursive -bor `
  [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::ContinueOnException
$list = [Alphaleonis.Win32.Filesystem.Directory]::EnumerateFileSystemEntries("c:\temp", '*', $searchOptions, [Alphaleonis.Win32.Filesystem.PathFormat]::FullPath)
# or
$list = [Alphaleonis.Win32.Filesystem.Directory]::EnumerateFileSystemEntries("c:\temp", '*', [System.IO.SearchOption]::AllDirectories, [Alphaleonis.Win32.Filesystem.PathFormat]::FullPath)

foreach ($path in $list) {
  $info = New-Object -TypeName "Alphaleonis.Win32.Filesystem.FileInfo" -ArgumentList (@$path, ([Alphaleonis.Win32.Filesystem.PathFormat]::FullPath))
  if ($info.Attributes -band [System.IO.FileAttributes]::Directory)
    { Write-Host ("Dir: " + $path) }
}

# PathFormat usage actually slightly increases performance (cursory tests show ~10% less time)
[Alphaleonis.Win32.Filesystem.Directory]::EnumerateDirectories("c:\temp", ([Alphaleonis.Win32.Filesystem.PathFormat]::FullPath))
[Alphaleonis.Win32.Filesystem.Directory]::EnumerateFiles("c:\temp", ([Alphaleonis.Win32.Filesystem.PathFormat]::FullPath))
```

Access methods comparison
```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Host.PrivateData.VerboseForegroundColor = [ConsoleColor]::DarkCyan

Import-Module (Join-Path -Path (Split-Path -Parent $MyInvocation.MyCommand.Path) -ChildPath "AlphaFS\lib\net40\AlphaFS.dll")

Function Invoke-GenericMethod {
Param(
  [Object]$Instance,
  [String]$MethodName,
  [Type[]]$TypeParameters,
  [Object[]]$MethodParameters
)
  Process {
    [Collections.ArrayList]$Private:parameterTypes = @{}
    ForEach ($Private:paramType In $MethodParameters) { [Void]$parameterTypes.Add($paramType.GetType()) }
    $Private:method = $Instance.GetMethod($methodName, "Instance, Static, Public", $Null, $parameterTypes, $Null)
    If ($Null -eq $method) { Throw ('Method not found: {0}.{1}' -f $Instance.ToString(), $methodName) }
    $method = $method.MakeGenericMethod($TypeParameters)
    $method.Invoke($Instance, $MethodParameters)
  }
}

function CalcDirectorySize1 {
[CmdletBinding()]
param(
  [string]$Path,
  [ref]$TotalDirs,
  [ref]$TotalFiles,
  [ref]$TotalSize
)
  $fsInfos = Invoke-GenericMethod `
    -Instance ([Alphaleonis.Win32.Filesystem.Directory]) `
    -MethodName "EnumerateFileSystemEntryInfos" `
    -TypeParameters @(([Alphaleonis.Win32.Filesystem.FileSystemEntryInfo])) `
    -MethodParameters (
      $path,
      ([Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::FilesAndFolders),
      ([Alphaleonis.Win32.Filesystem.PathFormat]::FullPath)
    )
  foreach ($fsInfo in $fsInfos) {
    if ($fsInfo.IsDirectory) {
      $TotalDirs.Value += 1
      CalcDirectorySize1 -Path $fsInfo.FullPath -TotalDirs $TotalDirs -TotalFiles $TotalFiles -TotalSize $TotalSize
    } else {
      $TotalFiles.Value += 1
      $TotalSize.Value += $fsInfo.FileSize
    } #if
  } #foreach
}

function CalcDirectorySize2 {
[CmdletBinding()]
param(
  [string]$Path,
  [ref]$TotalDirs,
  [ref]$TotalFiles,
  [ref]$TotalSize
)
  foreach ($Dir in [Alphaleonis.Win32.Filesystem.Directory]::EnumerateDirectories($Path, ([Alphaleonis.Win32.Filesystem.PathFormat]::FullPath))) {
    $TotalDirs.Value += 1
    CalcDirectorySize2 -Path $Dir -TotalDirs $TotalDirs -TotalFiles $TotalFiles -TotalSize $TotalSize
  } #foreach

  foreach ($File in [Alphaleonis.Win32.Filesystem.Directory]::EnumerateFiles($Path, ([Alphaleonis.Win32.Filesystem.PathFormat]::FullPath))) {
    $TotalFiles.Value += 1
    $TotalSize.Value += ([Alphaleonis.Win32.Filesystem.File]::GetFileSystemEntryInfo($File)).FileSize
  } #foreach
}

function CalcDirectorySize3 {
[CmdletBinding()]
param(
  [string]$Path,
  [ref]$TotalDirs,
  [ref]$TotalFiles,
  [ref]$TotalSize
)
  foreach ($Entry in [Alphaleonis.Win32.Filesystem.Directory]::EnumerateFileSystemEntries($Path, '*', [System.IO.SearchOption]::TopDirectoryOnly, [Alphaleonis.Win32.Filesystem.PathFormat]::FullPath)) {
    $EntryInfo = New-Object -TypeName "Alphaleonis.Win32.Filesystem.FileInfo" -ArgumentList @($Entry, ([Alphaleonis.Win32.Filesystem.PathFormat]::FullPath))
    if ($EntryInfo.Attributes -band [System.IO.FileAttributes]::Directory) {
      $TotalDirs.Value += 1
      CalcDirectorySize3 -Path $Entry -TotalDirs $TotalDirs -TotalFiles $TotalFiles -TotalSize $TotalSize
    } else {
      $TotalFiles.Value += 1
      $TotalSize.Value += $EntryInfo.Length
    } #if
  } #foreach
}

$TestPath = "c:\temp"

$TotalDirs = 0
$TotalFiles = 0
$TotalSize = ([int64]0)
$startTime = Get-Date

CalcDirectorySize1 -Path $TestPath -TotalDirs ([ref]$TotalDirs) -TotalFiles ([ref]$TotalFiles) -TotalSize ([ref]$TotalSize)

Write-Host ("Directories: {0}, files: {1}, total size: {2:n2} GB ({3})" -f $TotalDirs, $TotalFiles, ($TotalSize / 1Gb), $TotalSize)
Write-Host ((Get-Date) - $startTime)

$TotalDirs = 0
$TotalFiles = 0
$TotalSize = ([int64]0)
$startTime = Get-Date

CalcDirectorySize2 -Path $TestPath -TotalDirs ([ref]$TotalDirs) -TotalFiles ([ref]$TotalFiles) -TotalSize ([ref]$TotalSize)

Write-Host ("Directories: {0}, files: {1}, total size: {2:n2} GB ({3})" -f $TotalDirs, $TotalFiles, ($TotalSize / 1Gb), $TotalSize)
Write-Host ((Get-Date) - $startTime)

$TotalDirs = 0
$TotalFiles = 0
$TotalSize = ([int64]0)
$startTime = Get-Date

CalcDirectorySize3 -Path $TestPath -TotalDirs ([ref]$TotalDirs) -TotalFiles ([ref]$TotalFiles) -TotalSize ([ref]$TotalSize)

Write-Host ("Directories: {0}, files: {1}, total size: {2:n2} GB ({3})" -f $TotalDirs, $TotalFiles, ($TotalSize / 1Gb), $TotalSize)
Write-Host ((Get-Date) - $startTime)
```
Sample output
```
Directories: 36898, files: 406153, total size: 204,18 GB (219239243191)
00:00:30.8880000
Directories: 36898, files: 406153, total size: 204,18 GB (219239243191)
00:01:21.1668000
Directories: 36898, files: 406153, total size: 204,18 GB (219239243191)
00:02:05.2680000
```
