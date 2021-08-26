```batch
route print -4

route delete 0.0.0.0

:: use -p option to make a route persistent across reboots
route add 0.0.0.0 mask 0.0.0.0 192.168.0.1
```

```powershell
Get-NetAdapter
(Get-DnsClientServerAddress -InterfaceIndex 9 -AddressFamily IPv4).ServerAddresses
Set-DnsClientServerAddress -InterfaceIndex 9 -ServerAddresses @("192.168.0.1")
```
