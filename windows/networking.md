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
