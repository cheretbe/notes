(2check) How To Know Which Windows Version A Product Key Belongs To: https://github.com/Superfly-Inc/ShowKeyPlus/releases

Retrieve product key from BIOS
```powershell
wmic path softwarelicensingservice get OA3xOriginalProductKey
```
* https://www.nextofwindows.com/how-to-retrieve-windows-8-oem-product-key-from-bios

KMS activation

```batch
:: In the Office dir (e.g. C:\Program Files\Microsoft Office\Office14):
cscript ospp.vbs /sethst:kms.domain.tld
cscript ospp.vbs /setprt:portno
cscript ospp.vbs /act
:: Check license status
cscript ospp.vbs /dstatus

script slmgr.vbs -skms kms.domain.tld:portno
cscript slmgr.vbs -ato
:: Check status
:: [!!] Among other things, shows current KMS server
cscript slmgr.vbs -dlv
cscript slmgr.vbs -xpr
```

```powershell
  $licenseInfo = Get-WmiObject SoftwareLicensingProduct | Where-Object { $_.LicenseStatus -ne 0 }
  if ($licenseInfo.LicenseStatus -eq 1) {
    Write-Output ("{0}: Licensed" -f $licenseInfo.Description)
  } else {
    switch ($licenseInfo.LicenseStatus) {
      2 { $licenseStatusText = 'OOB Grace' }
      3 { $licenseStatusText = 'OOT Grace' }
      4 { $licenseStatusText = 'Non-Genuine Grace' }
      5 { $licenseStatusText = 'Notification' }
      6 { $licenseStatusText = 'Extended Grace' }
      else
        { $LicenseStatusText = 'Unknown' }
    } #switch
    Write-Output ("{0}: {1}" -f $licenseInfo.Description, $licenseStatusText)
    Write-Warning "Check activation status of the system"
  } #if
```
