:bulb: Use mbuffer instead
```shell
# mbuffer is in 'universe' repo
add-apt-repository universe
apt install mbuffer

# Small compressable files
# Receiver
mbuffer -q -4 -s 128k -m 1G -I 1234 | tar xvz
# Sender
tar cf - directory/ | pigz | mbuffer -q -s 128k -m 1G -O host.tld:1234

# No compression
# Receiver
mbuffer -q -4 -s 128k -m 1G -I 1234 | tar xv
# Sender
tar cf - directory/ | mbuffer -q -s 128k -m 1G -O host.tld:1234
```

:warning: 2test:
```shell
# receiver
mbuffer -4 -s 128k -m 1G -I 1234 | zfs receive -F pool/path
# sender
zfs send -R pool/path@snapshot | mbuffer -s 128k -m 1G -O dest-ip:1234
```

```shell
# on server
sudo apt install netcat
nc -l -p 1234 > /path/big_file.tar.gz

# on client
sudo apt install netcat pv
pv big_file.tar.gz | nc host.domain.tld 1234

# on server (receiver)
# -q seconds: after EOF is detected, wait the specified number of seconds and then quit
nc -q 1 -l -p 1234 | tar xv
# with current speed display (make sure pv is installed)
nc -q 1 -l -p 1234 | pv | tar x

# on client (sender)
tar cv . | nc -q 1 dest-ip 1234

# With pigz it's better to use pv on sender and -v on receiver
nc -q 1 -l -p 1234 | tar xvz
tar cf - directory/ | pv | pigz | nc host.domain.tld 1234
tar cf - /with/full/path/ | pv | pigz | nc host.domain.tld 1234
```
