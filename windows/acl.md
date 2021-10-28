* https://helgeklein.com/setacl/documentation/command-line-version-setacl-exe
```bat
:: -rec: for file system objects:
::       no (No recursion), cont (Recurse, and process directories only), obj (Recurse, and process files only)
::       cont_obj (Recurse, and process directories and files)
::       for registry objects: no (Do not recurse), yes (Do Recurse)
::       Recursion is not supported for other object types
SetACL.exe -actn list -ot file -rec cont_obj -on c:\path\to\a\directory
```
