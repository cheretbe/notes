* https://www.atlantic.net/community/howto/lock-down-your-centos-server-with-iptables/

```bash
# View status
service iptables status
# Edit rules
nano /etc/sysconfig/iptables
# Restart service 
service iptables restart
# List rules
iptables -S
```
