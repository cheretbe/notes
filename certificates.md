## Table of Contents
* [Unsorted](#unsorted)
* [Simple HTTPS Server in Python](#simple-https-server-in-python)
* [OpenSSL Commands](#open-ssl-commands)

###Unsorted
* GUI certificate viewer in linux: gcr-viewer
* https://www.outcoldman.com/en/archive/2016/05/15/os-x-server-web-server-proxy/
* https://github.com/diafygi/acme-tiny

###Simple HTTPS Server in Python
```python
# https://gist.github.com/dergachev/7028596
# https://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-with-self-signed-certificate

# Python 2
import BaseHTTPServer, SimpleHTTPServer
import ssl

# root privileges needed to listen to 443 port
httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='/path/to/cert_bundle.crt', keyfile='/path/to/private.key' server_side=True)
httpd.serve_forever()
```

###OpenSSL Commands
The Most Common OpenSSL Commands: https://www.sslshopper.com/article-most-common-openssl-commands.html

Extract the private key from the PFX
```
openssl pkcs12 -in {site}.pfx  -nocerts -nodes -passin pass:{password} | openssl rsa -out {site}.key
```
Extract the public key from the PFX
```
openssl pkcs12 –in {site}.pfx -clcerts -nokeys -passin pass:{password} | openssl x509 -out {site}.cer
```
Extract the chain bundle from the PFX
```
# [!]Note certificates order in the output file. Edit the file afterwards to put them in correct order
# Correct order: subject,[CA],CA
openssl pkcs12 -in archive.pfx -nodes -nokeys -passin pass:password -out chain.pem
# CA certificates only
openssl pkcs12 -in archive.pfx -nodes -nokeys -passin pass:password -cacerts -out chain.pem

# one more way to extract, -chain though is only valid for the pkcs12 subcommand
# and used when creating a PKCS12 keystore
openssl pkcs12 -in {site}.pfx -nodes -nokeys -cacerts -passin pass:{password} | openssl x509 -chain -out bundle.crt
```
