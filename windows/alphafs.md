* https://github.com/alphaleonis/AlphaFS
* https://github.com/alphaleonis/AlphaFS/wiki/PowerShell

`Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions`: `None` (do not use), `Files`, `Folders`, `FilesAndFolders`,
  `AsLongPath`, `SkipReparsePoints`, `ContinueOnException`, `Recursive`, `BasicSearch` (no short names), `LargeCache`

```powershell
$searchOptions = [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::Folders -bor `
  [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::SkipReparsePoints -bor `
  [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::Recursive -bor `
  [Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions]::ContinueOnException
$list = [Alphaleonis.Win32.Filesystem.Directory]::EnumerateFileSystemEntries("c:\temp", '*', $searchOptions)
# or
$list = [Alphaleonis.Win32.Filesystem.Directory]::EnumerateFileSystemEntries("c:\temp", '*', [System.IO.SearchOption]::AllDirectories)

foreach ($path in $list) {
  $info = New-Object -TypeName "Alphaleonis.Win32.Filesystem.FileInfo" -ArgumentList $path
  if ($info.Attributes -band [System.IO.FileAttributes]::Directory)
    { Write-Host ("Dir: " + $path) }
}

[Alphaleonis.Win32.Filesystem.Directory]::EnumerateDirectories("c:\temp")
[Alphaleonis.Win32.Filesystem.Directory]::EnumerateFiles("c:\temp")

```
