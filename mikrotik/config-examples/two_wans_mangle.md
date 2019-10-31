Set up external access from more than one wan interface
```
#add comment=wan1 distance=10 gateway=wan1
#add comment=wan2 distance=20 gateway=wan2
#/ip route rule
#add action=lookup-only-in-table routing-mark=wan2 table=wan2
#add action=lookup-only-in-table routing-mark=wan1 table=wan1
```

```
/ip firewall mangle
add action=mark-connection chain=input comment=\
    "Mark input connections from WAN1" in-interface=wan1 new-connection-mark=\
    wan1-input
add action=mark-connection chain=input comment=\
    "Mark input connections from WAN2" in-interface=wan2 new-connection-mark=\
    wan2-input
add action=mark-routing chain=output comment="Force outuput connections origin\
    ated from WAN1 to be routed through WAN1" connection-mark=wan1-input \
    new-routing-mark=wan1 passthrough=no
add action=mark-routing chain=output comment="Force outuput connections origin\
    ated from WAN2 to be routed through WAN2" connection-mark=wan2-input \
    new-routing-mark=wan2 passthrough=no
add action=mark-connection chain=forward comment=\
    "Mark connections forwarded from WAN1" connection-state=new in-interface=\
    wan1 new-connection-mark=wan1-pfw passthrough=no
add action=mark-connection chain=forward comment=\
    "Mark connections forwarded from WAN2" connection-state=new in-interface=\
    wan2 new-connection-mark=wan2-pfw passthrough=no
add action=mark-routing chain=prerouting comment=\
    "Force connections originated from WAN1 to be routed through WAN1" \
    connection-mark=wan1-pfw in-interface=lan-bridge new-routing-mark=wan1 \
    passthrough=no
add action=mark-routing chain=prerouting comment=\
    "Force connections originated from WAN2 to be routed through WAN2" \
    connection-mark=wan2-pfw in-interface=lan-bridge new-routing-mark=wan2 \
    passthrough=no

/ip route
add comment=wan2 distance=30 gateway=wan2 routing-mark=wan2
add comment=wan1 distance=30 gateway=wan1 routing-mark=wan1
```
