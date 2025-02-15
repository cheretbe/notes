```shell
#  -servername   Set TLS extension servername (SNI) in ClientHello (default)
# Essentially it works a little like a "Host" header in HTTP, i.e. it causes the requested domain name
# to be passed as part of the SSL/TLS handshake (in the SNI - Server Name Indication extension). A server
# can then host multiple domains behind a single IP. It will respond with the appropriate certificate base
# on the requested domain name.
# If you do not request a specific domain name the server does not know which certificate to give you, so you
# end up with a default one.
# https://stackoverflow.com/questions/43785703/using-servername-param-with-openssl-s-client/43787519#43787519
openssl s_client -servername www.godaddy.com -connect www.godaddy.com:443 -showcerts 2>/dev/null </dev/null | openssl x509 -text -issuer
# Expiration date
openssl s_client -servername www.godaddy.com -connect www.godaddy.com:443 2>/dev/null </dev/null | openssl x509 -noout -enddate | sed -e 's#notAfter=##' | xargs -i date -d "{}" +%d.%m.%Y

# Save cert bundle to a file
openssl s_client -connect www.godaddy.com:443 -showcerts </dev/null 2>/dev/null | sed -e '/-----BEGIN/,/-----END/!d' | tee temp/cert_chain.pem
# silent (useful for scripts)
openssl s_client -connect www.godaddy.com:443 -showcerts </dev/null 2>/dev/null | sed -e '/-----BEGIN/,/-----END/!d' | tee temp/cert_chain.pem >/dev/null
# save server cert bundle as separate files (reverse order - cert_1.pem is server itself; _2, etc - CAs)
openssl s_client -connect www.godaddy.com:443 -showcerts </dev/null 2>/dev/null | sed -e '/-----BEGIN/,/-----END/!d' | awk 'BEGIN {c=0;} /BEGIN CERT/{c++} { print > "cert_" c ".pem"}'
```

### Unsorted
* GUI certificate viewer in linux: gcr-viewer
* https://www.outcoldman.com/en/archive/2016/05/15/os-x-server-web-server-proxy/
* https://github.com/diafygi/acme-tiny
* Online SSL test: https://www.ssllabs.com/ssltest/
* **2review**
    * **https://github.com/cloudflare/cfssl** (https://blog.cloudflare.com/introducing-cfssl/)


### Container and Certificate types

* https://info.ssl.com/how-to-der-vs-crt-vs-cer-vs-pem-certificates-and-how-to-conver-them/
* https://myonlineusb.wordpress.com/2011/06/19/what-are-the-differences-between-pem-der-p7bpkcs7-pfxpkcs12-certificates/
* https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs
* https://stackoverflow.com/questions/1722181/how-to-determine-certificate-type-from-file/1726728#1726728

[X.509](https://en.wikipedia.org/wiki/X.509) is a standard defining the format of public key certificates.
There are several commonly used filename extensions for X.509 certificates. :warning: There is some overlap and other extensions are used, so one can’t always tell what kind of file they are working with just from looking at the file extension; one may need to open it and take a look for themselves.
* `.pem` – ([Privacy-enhanced Electronic Mail](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail)) Base64-encoded [DER](https://en.wikipedia.org/wiki/X.690#DER_encoding) certificate, enclosed between `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`
    * the PEM format solves the problem of transmitting binary files through systems, like electronic mail, that only support ASCII, by encoding the binary data using base64
    * PEM also defines a one-line header, consisting of `-----BEGIN `, a label, and `-----`, and a one-line footer, consisting of `-----END `, a label, and `-----`. The label determines the type of message encoded. Common labels include `CERTIFICATE`, `CERTIFICATE REQUEST`, `PRIVATE KEY` and `X509 CRL`
    * a single PEM file could contain an end-entity certificate, a private key, or multiple certificates forming a complete chain of trust
* `.cer`, `.crt`, `.der` – usually in binary [DER](https://en.wikipedia.org/wiki/X.690#DER_encoding) (Distinguished Encoding Rules) form
    * unlike PEM, DER-encoded files do not contain plain text statements such as `-----BEGIN CERTIFICATE-----`
    * some implementations accept a stream of DER encoded certs (a binary chain of concatenated DER certificates). But a better format would be PKCS#12 as it can be secured with a passphrase
* `.p12` – [PKCS#12](https://en.wikipedia.org/wiki/PKCS_12), an archive file format for storing many cryptography objects as a single file. It is commonly used to bundle a private key with its X.509 certificate or to bundle all the members of a chain of trust.
    * may contain certificate(s) (public) and private keys (password protected)
    * PKCS #12 is the successor to Microsoft's "PFX"; however, the terms "PKCS #12 file" and "PFX file" are sometimes used interchangeably
    * simpler, alternative format to PKCS #12 is PEM which just lists the certificates and possibly private keys as Base 64 strings in a text file
* `.p7b`, `.p7c` – [PKCS#7](https://en.wikipedia.org/wiki/PKCS_7) SignedData structure without data, just certificate(s) or CRL(s)
* `.pfx` – PFX, predecessor of PKCS#12
    * usually contains data in PKCS#12 format, e.g., with PFX files generated in IIS

### Let's Encrypt Certificate<a name="lets-encrypt-certificate"></a>
##### neilpang/acme.sh
* [letsencrypt.md](./letsencrypt.md)
##### Wildcard
Automated version: ../../tree/master/files/certbot

```shell
# Setup
pip install certbot

sudo snap install go --classic
export PATH=/snap/bin/go:$PATH
go install github.com/cloudflare/cloudflare-go/cmd/flarectl@latest

# Staging
# https://letsencrypt.org/docs/staging-environment/
# https://acme-staging-v02.api.letsencrypt.org/directory

cd temp
# [!!] Note multiple sub-domain entries
# Multiple level wildcard certificates are not implemented:
# https://community.letsencrypt.org/t/allow-multiple-level-wildcard-certificates/67242/2
certbot --logs-dir ./logs --config-dir ./conf --work-dir ./work \
  certonly --manual --preferred-challenges dns \
  --server https://acme-v02.api.letsencrypt.org/directory \
  -d *.domain.tld -d *.subdomain.domain.tld

export CF_API_EMAIL=user@domain.tld
export CF_API_KEY=0000000000000000000000000000000000000
go/bin/flarectl dns create -zone domain.tld --name _acme-challenge \
  -content 000000000000000000000000000-000000000000000 --type TXT

nslookup -type=TXT _acme-challenge.domain.tld

ls /etc/letsencrypt/live/domain.tld/fullchain.pem -lh
ls /etc/letsencrypt/live/chere.review/privkey.pem -lh

go/bin/flarectl dns list --zone domain.tld | grep _acme-challenge
go/bin/flarectl dns delete --zone domain.tld --id 00000000000000000000000000000000

# Renew
# [!!!] For manual renewal the original command needs to be run
# Because "certbot renew --manual" will work only with --manual-auth-hook,
# --manual-cleanup-hook and --manual-public-ip-logging-ok
```

* https://www.reddit.com/r/homelab/comments/8r575v/certbot_wildcard_automatic_dns_auth_with_amazon/
```shell
dig -t txt _acme-challenge.domain.tld @dns1.yandex.ru
nslookup -type=TXT _acme-challenge.domain.tld dns1.yandex.ru
```

##### Acme-tiny
* https://github.com/diafygi/acme-tiny
* https://stosb.com/blog/secure-your-letsencrypt-setup-with-acme-tiny/
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

##### Certbot

```shell
# --register-unsafely-without-email
# https://letsencrypt.org/docs/expiration-emails/
./certbot-auto register --agree-tos --no-eff-email --email <your@e-mail.address>
```

CentOS 7
```bash
sudo yum install epel-release
sudo yum install certbot
```
Add the following to `/etc/nginx/default.d/le-well-known.conf` file:
```
location ~ /.well-known {
        allow all;
}
```

```bash
systemctl restart nginx
# Default root path is /usr/share/nginx/html
certbot certonly -a webroot --webroot-path=/usr/share/nginx/html -d domain.tld -d www.domain.tld
```
Add certificate info to a config
```
server {
...
        ssl_certificate /etc/letsencrypt/live/domain.tld/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/domain.tld/privkey.pem;
...
}
```
```bash
# Check config
nginx -t
# Restart service
systemctl restart nginx
# Re-read config on cert change
systemctl reload nginx
# Edit cron file
export VISUAL=nano; crontab -e
```

From certbot's [docs](https://certbot.eff.org/all-instructions/): if you're setting up a cron or systemd job, we recommend running it twice per day (it won't do anything until your certificates are due for renewal or revoked, but running it regularly would give your site a chance of staying online in case a Let's Encrypt-initiated revocation happened for some reason). Please select a random minute within the hour for your renewal tasks.
```
# Check for SSL certificate renewal twice per day
19 0,12 * * * certbot renew --post-hook "systemctl reload nginx" --quiet
```

### Hardening HTTPS server

#### Apache
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

#### Nginx

```
server {
    listen 80;
    server_name *.domain.tld;
    rewrite ^ https://$host$request_uri? permanent;
}

server {
    listen 443 ssl;
    server_name site.domain.tld;
    ssl on;

    ssl_certificate /etc/nginx/ssl/site.domain.tld.bundle.crt;
    ssl_certificate_key /etc/nginx/ssl/site.domain.tld.key;

    ssl_protocols TLSv1.2 TLSv1.1 TLSv1;
    ssl_prefer_server_ciphers on;
    ssl_ciphers EECDH+ECDSA+AESGCM:EECDH+aRSA+AESGCM:EECDH+ECDSA+SHA512:EECDH+ECDSA+SHA384:EECDH+ECDSA+SHA256:ECDH+AESGCM:ECDH+AES256:DH+AESGCM:DH+AES256:RSA+AESGCM:!aNULL:!eNULL:!LOW:!RC4:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS;

    ssl_session_cache shared:TLS:2m;

    #Set HSTS to 365 days
    add_header Strict-Transport-Security 'max-age=31536000; includeSubDomains';

    # openssl dhparam 4096 -out /etc/nginx/ssl/dhparam.pem
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;

    root /var/www/test;
}
```

* Nginx SSL/TLS configuration for "A+" Qualys SSL Labs rating: https://gist.github.com/gavinhungry/7a67174c18085f4a23eb

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

### OpenSSL Commands
The Most Common OpenSSL Commands: https://www.sslshopper.com/article-most-common-openssl-commands.html

#### OpenSSL unable to write 'random state' error
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

On Linux comment out `RANDFILE` setting in `/etc/ssl/openssl.cnf` (https://stackoverflow.com/questions/63893662/cant-load-root-rnd-into-rng/63893731#63893731)

View certificates in a bundle (remove out the `-text` to just get subject/issuer info for each certificate)
```
openssl crl2pkcs7 -nocrl -certfile CHAINED.pem | openssl pkcs7 -print_certs -text -noout
```

Certificate chain for a site
```shell
openssl s_client -showcerts nl1.pointtoserver.com:443 </dev/null 2>/dev/null | openssl x509 -outform PEM >mycertfile.pem
openssl s_client -showcerts nl1.pointtoserver.com:443 </dev/null 2>/dev/null | openssl x509 -text
# Look for the following line
# CA Issuers - URI:http://crt.sectigo.com/SectigoRSADomainValidationSecureServerCA.crt
wget http://crt.sectigo.com/SectigoRSADomainValidationSecureServerCA.crt
openssl x509 -in SectigoRSADomainValidationSecureServerCA.crt -inform der -text

openssl s_client -showcerts nl1.pointtoserver.com:443 </dev/null | openssl x509 -out certdata

# Certificate Revocation List (CRL):
openssl x509 -in ServerCA.crt -inform der -text
# Check if the output contains something like
# X509v3 CRL Distribution Points: 
#   Full Name:
#     URI:http://crl.usertrust.com/USERTrustRSACertificationAuthority.crl

curl http://crl.usertrust.com/USERTrustRSACertificationAuthority.crl | openssl crl -inform DER -text -noout
# View CRL in PEM format
openssl crl -in /etc/openvpn/server/ca_crl.pem -text -noout
```
mikrotik
```
certificate crl add url=http://crl.usertrust.com/USERTrustRSACertificationAuthority.crl fingerprint=""
```


View request (CSR) file
```
openssl req -in mycsr.csr -noout -text
```

View certificate info
```shell
openssl x509 -in certificate.crt -text -noout
# SHA1 fingerprint
openssl x509 -in certificate.crt -noout -fingerprint
# Server cert fingerprint
openssl s_client -connect host.domain.tld:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -noout -in /dev/stdin
```

Verify certificate
```shell
openssl verify -untrusted /etc/letsencrypt/live/domain.tld/chain.pem /etc/letsencrypt/live/domain.tld/cert.pem
```

View (verify) certificates on server
```shell
openssl s_client -connect www.godaddy.com:443
echo | openssl s_client -servername www.godaddy.com -connect www.godaddy.com:443 2>/dev/null | openssl x509 -noout -enddate | sed -e 's#notAfter=##' | xargs -i date -d "{}" +%d.%m.%Y
```

Check if sertificate (or CSR) matches private key
```shell
openssl pkey -in privateKey.key -pubout -outform pem | sha256sum 
openssl x509 -in certificate.crt -pubkey -noout -outform pem | sha256sum 
openssl req -in CSR.csr -pubkey -noout -outform pem | sha256sum
# or
openssl rsa -in domain.tld.key -noout -modulus | openssl sha256
openssl x509 -in domain.tld.crt -noout -modulus| openssl sha256
```

Extract the private key from the PFX
```shell
# -passin pass:{password} for scripts
openssl pkcs12 -in domain.name.pfx -nocerts -nodes -out domain.name.key
#openssl pkcs12 -in {site}.pfx  -nocerts -nodes -passin pass:{password} | openssl rsa -out {site}.key
```
Extract the public key from the PFX
```shell
# -passin pass:{password} for scripts
openssl pkcs12 -in domain.name.pfx -clcerts -nokeys -out domain.name.crt
# openssl pkcs12 –in {site}.pfx -clcerts -nokeys -passin pass:{password} | openssl x509 -out {site}.cer
```
Extract the chain bundle from the PFX
```bash
# [!]Note certificates order in the output file. Edit the file afterwards to put them in correct order
# Correct order: subject,[CA],CA
openssl pkcs12 -in archive.pfx -nodes -nokeys -passin pass:password -out chain.pem
# CA certificates only
openssl pkcs12 -in archive.pfx -nodes -nokeys -passin pass:password -cacerts -out chain.pem

# one more way to extract, -chain though is only valid for the pkcs12 subcommand
# and used when creating a PKCS12 keystore
openssl pkcs12 -in {site}.pfx -nodes -nokeys -cacerts -passin pass:{password} | openssl x509 -chain -out bundle.crt

# Create PFX file from a certificate and a key
#   -certfile more.crt is optional, to include any additional certificates to the PFX file
openssl pkcs12 -export -out certificate.pfx -inkey privateKey.key -in certificate.crt -certfile more.crt
```

#### Import, export, convert between formats
```shell
# Convert PEM to DER
openssl x509 -outform der -in certificate.pem -out certificate.der
# Convert DER to PEM
openssl x509 -inform der -in certificate.cer -out certificate.pem
```

* https://www.sslshopper.com/ssl-converter.html
* https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs

### Own SSL Certificate Authority
* :warning: Use this: https://github.com/OpenVPN/easy-rsa
    * [./easy-rsa.md](./easy-rsa.md)
    * https://www.digitalocean.com/community/tutorials/how-to-set-up-and-configure-an-openvpn-server-on-ubuntu-20-04
* :bulb: and this (for development): https://github.com/FiloSottile/mkcert
* With Ansible (for serious automation): https://docs.ansible.com/ansible/latest/collections/community/crypto/docsite/guide_ownca.html
    * https://github.com/cheretbe/vagrant-files/blob/master/testlabs/ovpn-server/provision/server_provision.yml#L26
* (meh): https://smallstep.com/docs/step-ca/getting-started
    * https://github.com/smallstep/certificates
    * https://lobste.rs/s/1ddcvh/if_you_re_not_using_ssh_certificates_you_re
    * Advanced version: https://smallstep.com/blog/build-a-tiny-ca-with-raspberry-pi-yubikey/

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
# 7300 days is 20 years
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

### Adding a CA to Debian/Ubuntu
```shell
# Alternative:
# just copy .crt file to /usr/local/share/ca-certificates and run
update-ca-certificates --fresh

# Copy certificate to /usr/share/ca-certificates/ (use some custom subdirectory)
mkdir /usr/share/ca-certificates/custom
cp RapidSSLECCCA2018.crt /usr/share/ca-certificates/custom/RapidSSLECCCA2018.crt
# Edit /etc/ca-certificates.conf adding the following line
# custom/RapidSSLECCCA2018.crt
nano /etc/ca-certificates.conf
# Update CA certificates in /etc/ssl/certs/
update-ca-certificates --fresh
ls -lha /etc/ssl/certs/

# Check if a CA is present
find /etc/ssl/certs -iname '*.pem' -exec echo {} \; -exec openssl x509 -in {} -noout -fingerprint \; | grep '00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00'
```

### Adding a CA to CentOS

```shell
cp dummy.crt /etc/pki/ca-trust/source/anchors/
update-ca-trust
```

### Adding certificates to browsers on Linux
* https://chromium.googlesource.com/chromium/src/+/refs/heads/master/docs/linux/cert_management.md
* https://unix.stackexchange.com/questions/122753/chrome-certificate

```shell
# [!] GUI version
# chrome://settings/certificates?search=certificate
# Select "Authorities" > "Import"

sudo apt install libnss3-tools

# [!!] Use GUI version above
certutil -d sql:snap/chromium/current/.pki/nssdb/ -A -t TC -n "My CA" -i ~/Downloads/my_ca.crt 
# List certificates in the DB
certutil -L -d sql:snap/chromium/current/.pki/nssdb/
# For Firefox from snap
# sql:snap/firefox/common/.mozilla/firefox/0000000.default/
# For Chrome/Firefox from deb
# sql:$HOME/.pki/nssdb/

# [!!] Use GUI version above
# Чебурнет сертификаты
# https://www.gosuslugi.ru/crt
certutil -d sql:$HOME/.pki/nssdb/ -A -t TC -n "russian_trusted_root_ca" -i ~/Downloads/russian_trusted_root_ca_pem.crt
certutil -d sql:$HOME/.pki/nssdb/ -A -t TC -n "russian_trusted_sub_ca" -i ~/Downloads/russian_trusted_sub_ca_pem.crt
```

### Python code

* https://github.com/pyca/cryptography
```shell
pip install cryptography
```

```python
from cryptography import x509

with open("/path/to/a/cert/file.pem", "rb") as fh:
    pem_data = fh.read()
cert = x509.load_pem_x509_certificate(pem_data)
cert.serial_number
cert.extensions.get_extension_for_class(x509.KeyUsage).value
cert.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value._usages
```
