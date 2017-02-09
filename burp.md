Mailing list:

* [Bare-metal Windows 2008 R2 restore with secure key storage & without a Windows install disc](https://sourceforge.net/p/burp/mailman/message/35612245/)
* [burp server automated](https://sourceforge.net/p/burp/mailman/message/35605032/)
* [Incompatibility between 2.0.54 client and 1.3.48 server](https://sourceforge.net/p/burp/mailman/message/35648448/)
* [Small things after server upgrade](https://sourceforge.net/p/burp/mailman/message/35653928/)

The status monitor is now a client-side operation.
Please read http://burp.grke.org/docs/monitor.html and you will find out how
to make it work.

```
burp -c /etc/burp/burp-server.conf -t -C testclient | grep timer
```
