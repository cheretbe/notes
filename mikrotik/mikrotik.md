MTU on PPPoE: http://shop.duxtel.com.au/article_info.php?articles_id=26
```
export compact
# .rsc extension is added automatically
export compact file=config

:put [:resolve ya.ru]

/ip route print detail where dst-address="0.0.0.0/0" dynamic=yes
:put [/ip dhcp-server lease get [find host-name="host"] active-mac-address]
# Doesn't work if find returns several items
# :put [/system script get [/system script find] name]
# Need to iterate through items like this
:foreach sc in=[/system script find] do={ :put [/system script get $sc name] }

/ip route set [/ip route find where comment="ISP2"] disabled=yes

# full reset

/ip dhcp-client
add add-default-route=no disabled=no interface=ifname use-peer-dns=no use-peer-ntp=no


```
