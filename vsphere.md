#### Initial setup

```shell
docker run -dti -v ${HOME}/temp/powershell-root:/root -v ${HOME}/projects:/projects:ro --name powershell mcr.microsoft.com/powershell:preview-7.5-ubuntu-24.04 bash

docker exec -it powershell pwsh

apt update
apt install -y nano
nano /root/.config/powershell/Microsoft.PowerShell_profile.ps1
```

`/root/.config/powershell/Microsoft.PowerShell_profile.ps1` example
```powershell
Write-Output "Setting DNS server to 192.168.0.100"
@("nameserver 192.168.0.100", "search .") | Set-Content "/etc/resolv.conf"
Write-Output "Connecting to vsphere.domain.tld"
$cred = Import-CliXml -Path "/root/cred.xml"
Connect-VIServer -Server vsphere.domain.tld -Credential $cred
```

#### Orphaned disks
* http://www.vmwareadmins.com/finding-orphaned-vmdks-using-powercli/
```powershell
# tremendously slow, but seems to work
$arrUsedDisks = Get-VM | Get-HardDisk | %{$_.filename}
$arrUsedDisks += get-template | Get-HardDisk | %{$_.filename}
$arrDS = Get-Datastore
Foreach ($strDatastore in $arrDS)
{
    $strDatastoreName = $strDatastore.name
    $ds = Get-Datastore -Name $strDatastoreName | %{Get-View $_.Id}
    $fileQueryFlags = New-Object VMware.Vim.FileQueryFlags
    $fileQueryFlags.FileSize = $true
    $fileQueryFlags.FileType = $true
    $fileQueryFlags.Modification = $true
    $searchSpec = New-Object VMware.Vim.HostDatastoreBrowserSearchSpec
    $searchSpec.details = $fileQueryFlags
    $searchSpec.sortFoldersFirst = $true
    $dsBrowser = Get-View $ds.browser
    $rootPath = "["+$ds.summary.Name+"]"
    $searchResult = $dsBrowser.SearchDatastoreSubFolders($rootPath, $searchSpec)
    $myCol = @()
    foreach ($folder in $searchResult)
    {
        foreach ($fileResult in $folder.File)
        {
            $file = "" | select Name, FullPath 
            $file.Name = $fileResult.Path
            $strFilename = $file.Name
            IF ($strFilename)
            {
                IF ($strFilename.Contains(".vmdk")) 
                {
                    IF (!$strFilename.Contains("-flat.vmdk"))
                    {
                        IF (!$strFilename.Contains("delta.vmdk")) 
                        {
                            $strCheckfile = "*"+$file.Name+"*"
                            IF ($arrUsedDisks -Like $strCheckfile){}
                            ELSE 
                            { 
                                $strOutput = $strDatastoreName + " Orphaned VMDK Found: " + $strFilename
                                $strOutput
                            } 
                        }
                    } 
                }
            }
        }
    } 
}
```
