* https://helgeklein.com/setacl/documentation/command-line-version-setacl-exe
* https://helgeklein.com/download/
```bat
:: -ot: Type of object:
::      file: Directory/file, reg: Registry key, srv: Service, prn: Printer,
::      shr: Network share, wmi:WMI object
:: -rec: for file system objects:
::       no (No recursion), cont (Recurse, and process directories only), obj (Recurse, and process files only)
::       cont_obj (Recurse, and process directories and files)
::       for registry objects: no (Do not recurse), yes (Do Recurse)
::       Recursion is not supported for other object types
::
:: -actn list: Lists permissions. If -lst is omitted, a listing of the non-inherited permissions is created in
::             table format. The result can optionally be written to a backup file.
SetACL.exe -actn list -ot file -rec cont_obj -on c:\path\to\a\directory
```
