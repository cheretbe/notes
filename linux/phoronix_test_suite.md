Download links: http://www.phoronix-test-suite.com/?k=downloads
```shell
wget http://phoronix-test-suite.com/releases/repo/pts.debian/files/phoronix-test-suite_8.4.1_all.deb
dpkg -i phoronix-test-suite_8.4.1_all.deb 
apt-get install -f -q
ln -s /custom/location /var/lib/phoronix-test-suite

phoronix-test-suite list-all-tests
phoronix-test-suite install pts/compilebench
phoronix-test-suite run pts/compilebench
```
