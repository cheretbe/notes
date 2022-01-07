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
