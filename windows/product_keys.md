* KMS client setup keys: https://docs.microsoft.com/en-us/windows-server/get-started/kmsclientkeys
* NirSoft ProduKey: https://www.nirsoft.net/utils/product_cd_key_viewer.html

View product key contained in Windows installation media
```batch
md c:\mount

dism /Mount-Image /ImageFile:e:\sources\install.wim /Index:1 /MountDir:c:\mount /ReadOnly

:: [!] Run ProduKey as Administrator
:: "File" > "Select Source" > "Load the product keys from external Windows directory"
:: Browse for "C:\mount\Windows"

dism /Unmount-Image /MountDir:c:\mount /Discard
```

To change image to a higher edition and optionally enter a product key
```batch
dism /Mount-Image /ImageFile:e:\sources\install.wim /Index:1 /MountDir:c:\mount

dism /Image:c:\mount /Get-CurrentEdition
dism /Image:c:\mount /Get-TargetEditions

Dism /Image:c:\mount /Set-Edition:ServerDatacenterCor /AcceptEula /ProductKey:WMDGN-G9PQG-XVVXX-R3X43-63DFG

dism /Unmount-Image /MountDir:c:\mount /Commit
```
