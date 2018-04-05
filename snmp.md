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
