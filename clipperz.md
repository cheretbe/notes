* http://braincoop.devecoop.com/en/posts/password-management-with-clipperz.html
* http://fxpelive.ru/2015/06/13/kak-ustanovit-clipperz-v-ubuntu/

### SSL certificate

`SSLCertificateChainFile` will be deprecated since 2.4.8 (see https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslcertificatechainfile).
`SSLCertificateFile` with bundled intermediate certificates should be used instead. Find out Apache version: `apache2 -v`
