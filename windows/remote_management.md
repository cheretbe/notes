```powershell
# View event logs
# (!) Includes public profile
Enable-NetFirewallRule -Name RemoteEventLogSvc-In-TCP
```

* https://docs.microsoft.com/en-us/powershell/module/netsecurity/set-netfirewallservicefilter?view=win10-ps
```powershell
Get-NetFirewallRule -Name RemoteEventLogSvc-In-TCP | Get-NetFirewallServiceFilter
```
