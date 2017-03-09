## Table of Contents
* [Unsorted](#unsorted)
* [Let's Encrypt Certificate](#lets-encrypt-certificate)
* [Hardening HTTPS server](#Hardening-https-server)
* [Simple HTTPS Server in Python](#simple-https-server-in-python)
* [OpenSSL Commands](#openssl-commands)
* [Own SSL Certificate Authority](#own-ssl-certificate-authority)

### Unsorted
* GUI certificate viewer in linux: gcr-viewer
* https://www.outcoldman.com/en/archive/2016/05/15/os-x-server-web-server-proxy/
* https://github.com/diafygi/acme-tiny
* Online SSL test: https://www.ssllabs.com/ssltest/


[\[ TOC \]](#table-of-contents)

### Let's Encrypt Certificate<a name="lets-encrypt-certificate"></a>

``` shell
openssl genrsa 4096 > domain.key
# [!] Not the account key
openssl req -new -sha256 -key domain.key -subj "/CN=domain" -out domain.csr

mkdir -p .well-known/acme-challenge/
sudo python -m SimpleHTTPServer 80 &

git clone https://github.com/diafygi/acme-tiny.git

python3 acme-tiny/acme_tiny.py --account-key letsencrypt-account.key --csr domain.csr --acme-dir ./.well-known/acme-challenge/ > domain.pem

ps aux | grep python
sudo kill <process_id>

wget https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem

#check firewall rule
```

Multiple names. Create `domain.com.conf` file:
```
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
CN = www.domain.com

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = one.domain.com
DNS.2 = two.domain.com
DNS.3 = three.domain.com
```
Create the request:
```
openssl req -new -sha256 -key domain.com.key -config domain.com.conf -out domain.com.csr
```


https://xdeb.org/node/1614

[\[ TOC \]](#table-of-contents)


### Hardening HTTPS server

Apache
```apacheconf
# /etc/apache2/sites-available/default-ssl.conf
<IfModule mod_ssl.c>
  <VirtualHost _default_:443>
    # ...
    SSLProtocol ALL -SSLv2 -SSLv3
    SSLHonorCipherOrder On
    SSLCipherSuite ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL$

    <IfModule mod_headers.c>
      Header always set Strict-Transport-Security: "max-age=15768000"
    </IfModule>
  </VirtualHost>
</IfModule>

```
```
a2enmod headers
service apache2 restart
```

Sources:
* https://mozilla.github.io/server-side-tls/ssl-config-generator/
* https://xdeb.org/node/1614
* https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/

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

Command line version:
```shell
# Python 2
python -m SimpleHTTPServer [port]
# Python 3 (run python3 -m http.server --help for details)
python3 -m http.server [port]
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
