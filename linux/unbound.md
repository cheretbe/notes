```shell
# Filter log
journalctl -f -u unbound | grep "192.168.0.10" --line-buffered
# Set logging options without restarting
unbound-control set_option log-queries: yes
unbound-control set_option log-replies: yes
# To view resolved data DNSTAP needs to be enabled
https://github.com/NLnetLabs/unbound/issues/733
```
