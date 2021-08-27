* https://stackoverflow.com/questions/29937568/how-can-i-find-the-product-guid-of-an-installed-msi-setup/29937569
* https://stackoverflow.com/questions/48482545/how-can-i-compare-the-content-of-two-or-more-msi-files/48482546#48482546
* http://www.pantaray.com/msi_super_orca.html
* https://www.advancedinstaller.com/user-guide/qa-log.html
* :warning: patching and partial removal examples: https://www.adobe.com/devnet-docs/etk_deprecated/tools/AdminGuide/cmdline.html

Reboots
* http://exodusdev.com/products/whyreboot
* https://qtechbabble.wordpress.com/2020/06/26/use-pendingfilerenameoperations-registry-key-to-automatically-delete-a-file-on-reboot/

Product ID
* From an MSI
    * [Download](http://www.pantaray.com/msi_super_orca.html) SuperOrca
    * Open MSI file, select `Property` item on the left and find `ProductCode` property
* For an installed MSI
    * `get-wmiobject Win32_Product | Format-Table IdentifyingNumber, Name, LocalPackage -AutoSize`
    * Product ID is in IdentifyingNumber column
    
```powershell
$processObj = Start-Process msiexec.exe -Wait -PassThru `
  -ArgumentList "/i c:\temp\package.msi /passive /norestart SERVER=dummy SERVERACTIVE=dummy"
if ($processObj.ExitCode -ne 0)
    { Throw ("msiexec.exe call failed: exit code {0}" -f $processObj.ExitCode) }
```

1. To run with default settings just use `/passive` parameter
2. To find out parameters run through the installer with logging turned on and it will show all of the possible parameters that the specific MSI accepts
```batch
msiexec /log logfile.txt /i installer.msi
```
Search logfile.txt for passable parameters marked as "Property(S)" or "Property(C)" with the name in all caps (at the end of the file).
