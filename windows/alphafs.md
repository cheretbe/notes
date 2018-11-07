* https://github.com/alphaleonis/AlphaFS

`Alphaleonis.Win32.Filesystem.DirectoryEnumerationOptions`: `None` (do not use), `Files`, `Folders`, `FilesAndFolders`,
  `AsLongPath`, `SkipReparsePoints`, `ContinueOnException`, `Recursive`, `BasicSearch` (no short names), `LargeCache`

```
$dummy = [Alphaleonis.Win32.Filesystem.Directory]::EnumerateFileSystemEntries("c:\temp", '*', [System.IO.SearchOption]::AllDirectories)

```
