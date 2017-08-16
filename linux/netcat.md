```shell
# on server
sudo apt install netcat
nc -l -p 1234 > /path/big_file.tar.gz

# on client
sudo apt install netcat pv
pv big_file.tar.gz | nc host.domain.tld 1234

tar cvf - directory/ | pigz | nc host.domain.tld 1234
tar cvf - /with/full/path/ | pigz | nc host.domain.tld 1234

# on server
# -q seconds: after EOF is detected, wait the specified number of seconds and then quit
nc -q 1 -l -p 1234 | tar xv
# with current speed display (make sure pv is installed)
nc -q 1 -l -p 1234 | pv | tar x

# TODO: do some mbuffer tests
# https://unix.stackexchange.com/questions/48399/fast-way-to-copy-a-large-file-on-a-lan/48555#48555

# on client
tar cv . | nc -q 1 dest-ip 1234
```
