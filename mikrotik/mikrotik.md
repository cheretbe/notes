Installation Check-List
- [ ] Identity
- [ ] LAN address
- [ ] Default firewall rules
- [ ] NTP+timezone
- [ ] DNS server
- [ ] Scheduled task to save current config
- [ ] Disable autodiscovery on WAN (IP > Neighbours > Discovery Interfaces)


WLAN settings
- Band: 2GHz-B/G/N
- 20/40 MHz Ce
- Frequency: auto
- Mode: ap-bridge
- [Switch to advanced mode] Advanced > Distance: indoors


MTU on PPPoE: http://shop.duxtel.com.au/article_info.php?articles_id=26
```bash
export compact
# .rsc extension is added automatically
export compact file=config
# binary backup
/system backup save name="current.config"

:put [:resolve ya.ru]

/ip route print detail where dst-address="0.0.0.0/0" dynamic=yes
:put [/ip dhcp-server lease get [find host-name="host"] active-mac-address]
# Doesn't work if find returns several items
# :put [/system script get [/system script find] name]
# Need to iterate through items like this
:foreach sc in=[/system script find] do={ :put [/system script get $sc name] }

/ip route set [/ip route find where comment="ISP2"] disabled=yes

/interface pppoe-client monitor pppoe-if-name once do={ :put $"local-address" }

put [/ip firewall filter get [find comment="comment"] src-address]

# full reset
/system reset-configuration no-defaults=yes skip-backup=yes
/ip dhcp-client
add add-default-route=no disabled=no interface=ifname use-peer-dns=no use-peer-ntp=no
```

Seamless WiFi clients roaming (CAPsMAN):
* https://wiki.mikrotik.com/wiki/Manual:CAPsMAN
* https://serveradmin.ru/nastroyka-capsman-v-mikrotik/
* http://www.technotrade.com.ua/Articles/MikroTik_CAPsMAN_setup_2016-08-05.php
* http://odnakish.ru/2016/08/12/%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F-capsman-%D0%BE%D1%82-mikrotik-%D0%B1%D0%B5%D1%81%D1%88%D0%BE%D0%B2%D0%BD%D1%8B%D0%B9-%D1%80%D0%BE%D1%83%D0%BC%D0%B8%D0%BD%D0%B3-wi-fi/
* http://ithelp21.ru/nastroyka-capsmanv2-mikrotik-besshovny-rouming/
