Mikrotik OIDs
```
/interface print oid
/system identity print oid
/system resource print oid

SNMPv2-MIB::sysDescr.0 = STRING: RouterOS RB4011iGS+
SNMPv2-SMI::mib-2.47.1.1.1.1.2.65536 = STRING: "RouterOS 6.44.3 (stable) on RB4011iGS+"
```

```shell
sudo apt-get install snmp snmp-mibs-downloader
# Looks like this is called during snmp-mibs-downloader installation
sudo download-mibs
# Edit /etc/snmp/snmp.conf commenting out the `mibs :` line
# Make sure that MIBs are present
# -T TRANSOPTS Set various options controlling report produced:
#              ...
#              p:  print tree format symbol table
snmptranslate -Tp
```
https://l3net.wordpress.com/2013/05/12/installing-net-snmp-mibs-on-ubuntu-and-debian/

SNMP browsers
* http://www.ireasoning.com/download.shtml

```
snmpwalk -v 2c -c public 192.168.0.1
# On error "OID not increasing" use -Cc option
snmpwalk -Cc -v 2c -c public 192.168.0.1
```

Network interfaces and IPs
* http://oid-info.com/get/1.3.6.1.2.1.2.2.1.1
* http://oid-info.com/get/1.3.6.1.2.1.2.2.1.2
* http://oid-info.com/get/1.3.6.1.2.1.4.20.1.2
* http://oid-info.com/get/1.3.6.1.2.1.4.20.1.1

Public SNMP simulation service
* http://snmplabs.com/snmpsim/public-snmp-agent-simulator.html

```shell
# List interfaces
snmptable -c public -v 2c demo.snmplabs.com .1.3.6.1.2.1.2.2
# List IP addresses
snmptable -c public -v 2c demo.snmplabs.com .1.3.6.1.2.1.4.20
```
