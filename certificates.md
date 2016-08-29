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
openssl pkcs12 -in {site}.pfx -nodes -nokeys -cacerts -passin pass:{password} | openssl x509 -chain -out bundle.crt
```
