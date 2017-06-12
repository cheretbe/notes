```shell
# on server
sudo apt install netcat
nc -l -p 7000 > /path/big_file.tar.gz

# on client
sudo apt install netcat pv
pv big_file.tar.gz | nc host.domain.tld 7000


# on server
nc -q 1 -l -p 1234 | tar xv

# on client
tar cv . | nc -q 1 dest-ip 1234
```
