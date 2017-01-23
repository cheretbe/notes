## Table of Contents
* [Unsorted](#unsorted)
* [Simple HTTPS Server in Python](#simple-https-server-in-python)
* [OpenSSL Commands](#openssl-commands)
* [Own SSL Certificate Authority](#own-ssl-certificate-authority)

### Unsorted
* GUI certificate viewer in linux: gcr-viewer
* https://www.outcoldman.com/en/archive/2016/05/15/os-x-server-web-server-proxy/
* https://github.com/diafygi/acme-tiny
* Online SSL test: https://www.ssllabs.com/ssltest/

[\[ TOC \]](#table-of-contents)

### Simple HTTPS Server in Python
```python
# https://gist.github.com/dergachev/7028596
# https://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-with-self-signed-certificate

# Python 2
import BaseHTTPServer, SimpleHTTPServer
import ssl

# root privileges are needed to listen to 443 port
httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='/path/to/cert_bundle.crt', keyfile='/path/to/private.key', server_side=True)
httpd.serve_forever()

# Python 3
import http.server
import ssl

httpd = http.server.HTTPServer(('localhost', 4443), http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='/path/to/cert_bundle.crt', keyfile='/path/to/private.key', server_side=True)
httpd.serve_forever()
```
[\[ TOC \]](#table-of-contents)

### OpenSSL Commands
The Most Common OpenSSL Commands: https://www.sslshopper.com/article-most-common-openssl-commands.html

#### OpenSSL unable to write 'random state' error <a name="openssl-random-state-error"></a>
When running non-elevated on Windows openssl.exe shows the following error: `unable to write 'random state'`. 
OpenSSL on Windows tries to save the 'random state' file in the following order:
  1. Path taken from RANDFILE environment variable
  2. If HOME environment variable is set then : ${HOME}\.rnd
  3. C:\.rnd

Since by default HOME is not set, it tries to write `C:\.rnd` and fails. The solution to set either RANDFILE or HOME variable:
```bat
SET RANDFILE=.rnd
:: or
SET HOME=%HOMEPATH%
```

View certificates on server
```
openssl s_client -connect www.godaddy.com:443
```

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
[\[ TOC \]](#table-of-contents)

### Own SSL Certificate Authority

This is for simplistic approach when CA signs server or client certificates directly. For more advanced and secure approach with intermediate CAs, database to keep track of signed certificates, etc. see this guide: https://jamielinux.com/docs/openssl-certificate-authority/introduction.html

The solution to `unable to write 'random state'` error on Windows is [here](#openssl-random-state-error).

Create the Root Key
```shell
# 4096 bits is for root certificate only. It will be possible to
# sign server and client certificates of a shorter length
openssl genrsa -aes256 -out ca.key.pem 4096
```
Create the root certificate
```shell
# 7200 days is 20 years
openssl req -key ca.key.pem -new -x509 -days 7300 -sha256 -out ca.cert.pem
# Verify it
openssl x509 -noout -text -in ca.cert.pem
```
Export to DER format to use on Windows machines (or just rename .pem to .crt)
```shell
openssl x509 -in ca.cert.pem -outform DER -out ca.cer
```
Issue a device certificate
```shell
# Create a private key
openssl genrsa -out device.key 2048
# Generate a certificate signing request (leave challenge password empty)
openssl req -new -key device.key -out device.csr
# Create a singned certificate
# -CAcreateserial: CA serial number file is created if it does not exist. It will contain the
#                  serial number "02" and the certificate being signed will have the 1 as its
#                  serial number. Normally if the -CA option is specified and the serial number
#                  file does not exist it is an error.
openssl x509 -req -in device.csr -CA ca.cert.pem -CAkey ca.key.pem -CAcreateserial -out device.crt -days 3650 -sha256
```
Sertificate reques with alternative names: http://blog.endpoint.com/2014/10/openssl-csr-with-alternative-names-one.html

Sources:
* https://datacenteroverlords.com/2012/03/01/creating-your-own-ssl-certificate-authority/
* http://blog.endpoint.com/2014/10/openssl-csr-with-alternative-names-one.html

[\[ TOC \]](#table-of-contents)
