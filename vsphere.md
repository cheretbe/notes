#### Initial setup

```shell
docker run -dti -v ${HOME}/temp/powershell-root:/root -v ${HOME}/projects:/projects:ro --name powershell mcr.microsoft.com/powershell:preview-7.5-ubuntu-24.04 bash

docker exec -it powershell pwsh

Install-Module -Name VMware.PowerCLI -Force
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$FALSE
Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $FALSE -Confirm:$FALSE

apt update
apt install -y nano

$cred = Get-Credential -UserName "user@domain.tld"
$cred | Export-CliXml -Path "/root/cred.xml"

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
Set-StrictMode -Version Latest
$ErrorActionPreference = [System.Management.Automation.ActionPreference]::Stop

$dsVMFiles = Get-DatastoreCluster -Name "dc2-devops-iscsi-02-ssd-cluster" | Get-VM | Get-HardDisk | %{$_.filename}

$totalSize = 0

$dsCluster = Get-DatastoreCluster -Name "dc2-devops-iscsi-02-ssd-cluster"
foreach ($ds in (Get-Datastore | where { $_.ExtensionData.Parent -eq $dsCluster.Id })) {
    $dsView = Get-View $ds.id
    $fileQueryFlags = New-Object VMware.Vim.FileQueryFlags
    $fileQueryFlags.FileSize = $true
    $fileQueryFlags.FileType = $true
    $fileQueryFlags.Modification = $true
    $searchSpec = New-Object VMware.Vim.HostDatastoreBrowserSearchSpec
    $searchSpec.details = $fileQueryFlags
    $searchSpec.sortFoldersFirst = $true
    $dsBrowser = Get-View $dsView.browser
    $rootPath = "["+$dsView.summary.Name+"]"
    $searchResult = $dsBrowser.SearchDatastoreSubFolders($rootPath, $searchSpec)

    foreach ($folder in $searchResult) {
        foreach ($fileResult in $folder.File) {
            $fullPath = ("{0}{1}" -f $folder.FolderPath , $fileResult.Path)
            if (($fileResult.Path | Split-Path -Extension) -in @(".vmdk")) {
                if (-not ($fullPath -in $dsVMFiles)) {
                    $fullPath
                    $totalSize += $fileResult.FileSize
                } #if
            } #if
        }
    }
}

("Total size: {0}" -f $totalSize)
```

```powershell
# https://vprhlabs.blogspot.com/2016/07/move-vm-files-between-datastore-using.html
# Didn't actually work, failed on a couple of *-ctk.vmdk files. Didn't try on anything else 

Connect-VIServer vcenter-server

$dstDatastore = Get-Datastore destination-Datastore-Name
New-PSDrive -PSProvider VimDatastore -Root "\"  -location $dstDatastore -Name dstDS

$vmdks = Import-Csv c:\temp\vmdk-folders.csv
foreach ( $vmdk in $vmdks ) { 
  Write-Host Moving $vmdk.vmdkfolder from $vmdk.datastore....
  $srcDatastore = Get-Datastore $vmdk.datastore
  $vmdkfolder = $vmdk.vmdkFolder
  New-PSDrive -PSProvider VimDatastore -Root "\"  -location $srcDatastore -Name srcDS
  Move-Item srcDs:\$vmdkfolder -Destination dstDS:\
  Remove-PSDrive -Name srcDS
}

Remove-PSDrive -Name dstDS
```
