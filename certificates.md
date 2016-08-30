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
openssl pkcs12 -in archive.pfx -nodes -nokeys -passin pass:password -out chain.pem
# CA certificates only
openssl pkcs12 -in archive.pfx -nodes -nokeys -passin pass:password -cacerts -out chain.pem

# one more way to extract, -chain though is only valid for the pkcs12 subcommand
# and used when creating a PKCS12 keystore
openssl pkcs12 -in {site}.pfx -nodes -nokeys -cacerts -passin pass:{password} | openssl x509 -chain -out bundle.crt
```
