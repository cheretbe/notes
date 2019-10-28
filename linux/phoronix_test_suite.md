* Check out stress-ng
    * https://ruhighload.com/%D0%A1%D1%82%D1%80%D0%B5%D1%81%D1%81-%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5+%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BE%D0%B2+%D1%81+%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E+stress-ng


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

* phoronix-cmd.md: https://gist.github.com/anshula/728a76297e4a4ee7688d
* https://www.phoronix.com/forums/forum/phoronix/phoronix-test-suite/901127-documentation-confusion-getting-started
