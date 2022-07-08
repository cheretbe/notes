```batch
route print -4

route delete 0.0.0.0

:: use -p option to make a route persistent across reboots
route add 0.0.0.0 mask 0.0.0.0 192.168.0.1

powershell.exe "Invoke-RestMethod https://freegeoip.app/json; Write-Host "Press any key..."; $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown') | Out-Null"
```

```powershell
Get-NetAdapter
(Get-DnsClientServerAddress -InterfaceIndex 9 -AddressFamily IPv4).ServerAddresses
# [!!!] This setting is permanent
Set-DnsClientServerAddress -InterfaceIndex 9 -ServerAddresses @("192.168.0.1")
# To reset the DNS server IP addresses to the default value
Set-DnsClientServerAddress -InterfaceIndex 9 -ResetServerAddresses

Invoke-RestMethod https://freegeoip.app/json
```

Set custom DHCP client ID
```powershell
$client_id="v12345678"

$hexified=[System.Text.Encoding]::ASCII.GetBytes($client_id)
$objWin32NAC = Get-WmiObject -Class Win32_NetworkAdapterConfiguration -namespace "root\CIMV2" -computername "." -Filter "IPEnabled = 'True' AND DHCPEnabled ='True'"
foreach ($objNACItem in $objWin32NAC) {
  $nic = ($objNACItem.SettingID)
  New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\services\Tcpip\Parameters\Interfaces\$nic -Force -Name DhcpClientIdentifier -PropertyType Binary -Value ([byte[]]$hexified)
 }
 Write-Host $nic
 Write-Host $hexified
```
* https://vmind.ru/2018/02/01/dhcp-option-61-clientid-windows10/
* 
