* https://stackoverflow.com/questions/29937568/how-can-i-find-the-product-guid-of-an-installed-msi-setup/29937569
* https://stackoverflow.com/questions/48482545/how-can-i-compare-the-content-of-two-or-more-msi-files/48482546#48482546
* http://www.pantaray.com/msi_super_orca.html

Product ID
* From an MSI
    * [Download](http://www.pantaray.com/msi_super_orca.html) SuperOrca
    * Open MSI file, select `Property` item on the left and find `ProductCode` property
* For an installed MSI
    * `get-wmiobject Win32_Product | Format-Table IdentifyingNumber, Name, LocalPackage -AutoSize`
    * Product ID is in IdentifyingNumber column
