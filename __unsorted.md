```
PS C:\Users\Администратор.GUR> Get-WinEvent -ListLog * -EA silentlycontinue | where-object { $_.recordcount -AND $_.last
writetime -gt [datetime]::today} | foreach-object { get-winevent -FilterHashtable @{logname=$_.logname; starttime=((Get-
Date) - (New-TimeSpan -Minutes 10))} -EA SilentlyContinue} | Format-List | Out-String -Stream -width 4096 | Out-File 'C:
\temp\events.txt' -Width 4096
```
