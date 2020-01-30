2review:
* https://wiki.mikrotik.com/wiki/Manual:VRRP-examples

Installation Check-List
- [ ] Identity
- [ ] Admin username/password
- [ ] LAN address
- [ ] Default firewall rules
- [ ] NTP+timezone
- [ ] DNS server
- [ ] Scheduled task to save current config
- [ ] Disable autodiscovery on WAN (`IP` > `Neighbours` > `Discovery Interfaces`. New ROS uses lists, defined in `Interfaces` > `Interface List`)
- [ ] Review https://wiki.mikrotik.com/wiki/Manual:Securing_Your_Router


WLAN settings
- Band: 2GHz-B/G/N
- 20/40 MHz Ce
- Frequency: auto
- Mode: ap-bridge
- [Switch to advanced mode] Advanced > Distance: indoors
- (2check): https://blog.ligos.net/2018-01-01/Mikrotik-WiFi-Access-Point-With-VLAN.html
- Ppoint-to-point bridge: https://www.technotrade.com.ua/Articles/mikrotik_wifi_bridge_setup_2013-09-08.php

Winbox settings location: ` %USERPROFILE%\AppData\Roaming\Mikrotik\Winbox`

Get latest RoS version:
```shell
curl http://download2.mikrotik.com/routeros/LATEST.6
# 6.41.2 1517920142
```

MTU on PPPoE: http://shop.duxtel.com.au/article_info.php?articles_id=26
```bash
# View default config
/system default-configuration print
# .txt extension added automatically
/system default-configuration print file=default-config

# View current config
/export compact
# .rsc extension is added automatically
/export compact file=config

# binary backup
/system backup save name="current.config"

# Quick sniffer
/tool sniffer quick ip-protocol=icmp ip-address=192.168.0.129,192.168.0.1

# [!!] Full reset
/system reset-configuration no-defaults=yes skip-backup=yes
/interface ethernet print
# VM
/interface ethernet reset-mac-address ether1
/interface ethernet set ether1 mac-address=xxx
/ip dhcp-client
add add-default-route=no disabled=no interface=ifname use-peer-dns=no use-peer-ntp=no

:put [:resolve ya.ru]

/ip route print detail where dst-address="0.0.0.0/0" dynamic=yes
:put [/ip dhcp-server lease get [find host-name="host"] active-mac-address]
# Doesn't work if find returns several items
# :put [/system script get [/system script find] name]
# Need to iterate through items like this
:foreach sc in=[/system script find] do={ :put [/system script get $sc name] }

# Delete all firewall rules
/ip firewall filter remove [/ip firewall filter find]

# Move last rule to the top
/ip firewall nat move ([:len [/ip firewall nat find]] - 1) 0

foreach ff in=[/ip firewall filter find] do={ :put [/ip firewall filter get $ff src-address] }
# All properties
foreach ff in=[/ip firewall filter find] do={ :put [/ip firewall filter get $ff] }

:local lastRuleIdx
:set lastRuleIdx ([:len [/ip firewall filter find]] - 1)  
:put [:pick [/ip firewall filter find] $lastRuleIdx]

/ip route set [/ip route find where comment="ISP2"] disabled=yes

/interface pppoe-client monitor pppoe-if-name once do={ :put $"local-address" }

put [/ip firewall filter get [find comment="comment"] src-address]

:put [/ip firewall nat find action=masquerade and out-interface="wan"]
:put [/ip firewall nat find action=masquerade or out-interface="wan"]

# Minimal valid date is Jan/01/1970
```
#### Logging
```
:if ([:len [/system logging find topics="script;debug"]] = 0) do={ /system logging add topics=script,debug }
:if ([/system logging get [find topics="script;debug"] disabled]) do={ /system logging set [find topics="script;debug"] disabled=no }

:log warning "Warning test"
:log debug "Debug test"

/log print where topics~"script"
/log print where topics="script;debug"

:foreach entry in=[/log find topics~"script;debug"] do={:put [/log get $entry] }
:foreach entry in=[/log find topics~"script"] do={:put [/log get $entry] }
:foreach entry in=[/log find topics~"script"] do={:put [/log get $entry message] }
```
#### Scripts

* **TODO:** add `:tostr`, `:pick` etc. examples (http://www.mikrotik-routeros.com/2014/10/scriptlet-find-default-route-interface-names-and-a-free-licence/#more-1052)

```shell
:if ([/interface ethernet get [find mac-address="$lanMACaddr"] name] != "lan") do={
  :put "Setting '$lanMACaddr' interface name to 'lan'"
  /interface ethernet set [find mac-address="$lanMACaddr"] name="lan"
}

:if ([:len [/interface find name="wan1"]] != 0) do={
  :put "'wan1' interface is present"
} else {
  :put "'wan1' interface is not present"
}

:if ([:len [/routing ospf interface find interface="inter_isp"]] = 0) do={
  :put "Adding OSPF with hello-interval of 1s on interface 'inter_isp'"
  /routing ospf interface add hello-interval=1s interface=inter_isp
} else={
  if ([/routing ospf interface get [find interface="inter_isp"] hello-interval] != "00:00:01") do={
    :put "Changing OSPF hello-interval to 1s on interface 'inter_isp'"
    /routing ospf interface set [find interface="inter_isp"] hello-interval=1s
  }
}

# Download a script and run it without saving to file
# (seems to work with files > 4096 bytes in size)
[:parse ([/tool fetch mode=https url="https://raw.githubusercontent.com/cheretbe/mikrotik-scripts/master/failover/failover_setup.rsc" output=user as-value]->"data")]

/system script add name= script1 source=[/file get script1.rsc contents]
/system script set script1 source=[/file get script.txt contents]
/system script run script1
/system script edit value-name=source <script name>

/file edit value-name=contents test1.txt

# Next line is a workaround to create a file
/file print file=script1
/file set script1 contents=[/system script get script1 source]

# auto.rsc feature - using ftp you can upload file called <something>.auto.rsc, script
# file will be automatically executed and log file for that will be saved on the router.
# It might be worth noting that the script does not execute immediately upon upload. It
# executes when the ftp connection is closed. A not so subtle detail.

:put [/terminal inkey ]

:set varname test
/system script environment set $varname value=bbb
```
* http://mikrotik.net.pl/wiki/Scripty
* http://wiki.mikrotik.com/wiki/Manual:Scripting
* http://wiki.mikrotik.com/wiki/Manual:Scripting-examples
* http://wiki.mikrotik.com/wiki/Failover_Scripting
* http://forum.mikrotik.com/viewtopic.php?f=9&t=75810
* http://forum.mikrotik.com/viewtopic.php?t=51229

#### SSTP
```
/certificate add common-name=CA_name days-valid=3650 name=CA key-usage=crl-sign,key-cert-sign
/certificate sign CA
/certificate add name="SSTP Server" days-valid=3650 common-name=host1.domain.tld subject-alt-name=DNS:host2.domain.tld,IP:192.168.0.1,IP:192.168.1.1 key-usage=digital-signature,key-encipherment,tls-server
/certificate sign "SSTP Server" ca=CA

/certificate import file-name=ca.crt passphrase=""
```

#### Seamless WiFi clients roaming (CAPsMAN):
```
/interface wireless cap
set discovery-interfaces=ether1 enabled=yes interfaces=wlan1
```
:warning: On the same device do not use `discovery interfaces`, set `CAPsMAN Addresses` to 127.0.0.1 and allow 5246,5247/UDP traffic (127.0.0.1 -> 127.0.0.1) in the firewall 

* https://wiki.mikrotik.com/wiki/Manual:CAPsMAN
* https://serveradmin.ru/nastroyka-capsman-v-mikrotik/
* http://www.technotrade.com.ua/Articles/MikroTik_CAPsMAN_setup_2016-08-05.php
* http://odnakish.ru/2016/08/12/%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F-capsman-%D0%BE%D1%82-mikrotik-%D0%B1%D0%B5%D1%81%D1%88%D0%BE%D0%B2%D0%BD%D1%8B%D0%B9-%D1%80%D0%BE%D1%83%D0%BC%D0%B8%D0%BD%D0%B3-wi-fi/
* http://ithelp21.ru/nastroyka-capsmanv2-mikrotik-besshovny-rouming/

```
/interface ppp-client
add apn=internet.beeline.ru data-channel=1 dial-on-demand=no disabled=no \
    info-channel=2 modem-init="AT+CGDCONT=1,\"IP\",\"internet.beeline.ru\"" 
    name=ppp-out1 password=beeline phone=*99***1# port=usb2 user=beeline

# newer version
# note "dial-on-demaind" when testing
/interface ppp-client
add add-default-route=no apn=internet.beeline.ru data-channel=1 dial-on-demand=\
    no info-channel=2 name=ppp-beeline password=beeline phone=*99# port=usb1 \
    use-peer-dns=no user=beeline

/system routerboard usb power-reset duration=5s
```
View modem/operator info
```
/interface ppp-client info ppp-client1
# or "Info" button in ppp interface properties
```
```
# Set/view CD mode
system serial-terminal port=usb1 channel=2
# View autorun state:
AT+ZCDRUN=4
# enable:
AT+ZCDRUN=9
# disable:
AT+ZCDRUN=8

# View download mode (most likely not needed)
AT+ZCDRUN=G
# enable:
AT+ZCDRUN=E
# disable:
AT+ZCDRUN=F
```
* https://habr.com/post/188424/
* https://christian.amsuess.com/tutorials/zte_mf180/

Как задать статический маршрут в случае, если ppp сервер не назначает параметр "remote address": задать вручную любой удобный ip адрес в этом поле в свойствах соединения и указать его в качестве шлюза в маршруте.

* http://mybroadband.co.za/vb/showthread.php/400897-MikroTik-RouterBoard-and-USB-3G-Modems/page6

#### SNMP

* https://wiki.mikrotik.com/wiki/Manual:SNMP

```
/snmp set enabled=yes
```

```shell
# View interface list (indices)
snmpwalk -Os -c public -v 2c ip-addr .1.3.6.1.2.1.2.2.1.1
# View interface names
snmpwalk -Os -c public -v 2c ip-addr .1.3.6.1.2.1.2.2.1.2
# View interface indices for IP addresses
snmpwalk -Os -c public -v 2c ip-addr .1.3.6.1.2.1.4.20.1.2
# View IP address list
snmpwalk -Os -c public -v 2c ip-addr .1.3.6.1.2.1.4.20.1.1

# For snmptable to work standart MIBs have to be installed:
# https://github.com/cheretbe/notes/blob/master/snmp.md
# View as a table
# Interfaces
snmptable -c public -v 2c ip-addr .1.3.6.1.2.1.2.2
# IP addresses
snmptable -c public -v 2c ip-addr .1.3.6.1.2.1.4.20
```
* http://oid-info.com/get/1.3.6.1.2.1.2.2.1.1
* http://oid-info.com/get/1.3.6.1.2.1.2.2.1.2
* http://oid-info.com/get/1.3.6.1.2.1.4.20.1.2
* http://oid-info.com/get/1.3.6.1.2.1.4.20.1.1

#### OSPF
* https://mum.mikrotik.com/presentations/CR18/presentation_5632_1532409246.pdf
* https://youtu.be/u_V2FdcpQLM

### RoMON
```
/ip neighbor print
/tool mac-telnet 00:00:00:00:00:00
/tool romon print
/tool romon set enabled=yes
```
* https://wiki.mikrotik.com/wiki/Manual:RoMON
