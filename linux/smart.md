### Smartd settings

Uncomment the line in `/etc/default/smartmontools`:
```
start_smartd=yes
```


Config file `/etc/smartd.conf`:
```apache
# -a     default: equivalent to -H -f -t -l error -l selftest -C 197 -U 198
# -H     monitor SMART Health Status, report if failed
# -f     monitor for failure of any 'Usage' Attributes
# -t     equivalent to -p and -u directives
# -p     report changes in 'Prefailure' Normalized Attributes
# -u     report changes in 'Usage' Normalized Attributes
# -l     monitor SMART log (error, selftest)
# -C 197 report if Current Pending Sector count non-zero
# -U 198 report if Offline Uncorrectable count non-zero
# -S on  enable attribute autosave
# -o on  enable automatic offline tests
# -I 194 ignore tempature
# -I 9   ignore poweron hours
# -m     send warning email to   
# -s     self-test schedule, short selftests every morning after 04:00 and long selftests Saturdays after 05:00
DEVICESCAN -a -S on -o on -I 194 -I 9 -m notifications@domain.tld -s (S/../.././04|L/../../6/05)
# Add ‘-M test’ parameter to send test message on daemon start
```
