```bash
# View info for all drives
smartctl --scan | awk '{ print "########## " $1 " ##########"; system ("smartctl -i " $1) }'
smartctl --scan | awk '{ print "########## " $1 " ##########"; system ("smartctl -A " $1 "| grep -i sector") }'
smartctl --scan | awk '{ print "########## " $1 " ##########"; system ("smartctl -a " $1 "| grep -ie sector -ie error") }' | less

# Or use check_smart script
check_smart_ver=$(curl -s https://api.github.com/repos/Napsty/check_smart/releases/latest | jq -r ".tag_name")
wget https://github.com/Napsty/check_smart/archive/${check_smart_ver}.tar.gz
tar -xzvf ${check_smart_ver}.tar.gz
cd check_smart-${check_smart_ver}/

check_smart.pl -g '/dev/sd[a-g]' -i auto
```

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
