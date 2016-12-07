http://www.windowscentral.com/how-create-windows-10-iso-file-using-installesd-image

``` bash
# /etc/dhcp/dhclient.conf
# supersede domain-name-servers 8.8.8.8, 8.8.4.4;
dhclient -x
dhclient
```

```
PS C:\Users\Администратор.GUR> Get-WinEvent -ListLog * -EA silentlycontinue | where-object { $_.recordcount -AND $_.last
writetime -gt [datetime]::today} | foreach-object { get-winevent -FilterHashtable @{logname=$_.logname; starttime=((Get-
Date) - (New-TimeSpan -Minutes 10))} -EA SilentlyContinue} | Format-List | Out-String -Stream -width 4096 | Out-File 'C:
\temp\events.txt' -Width 4096
```
