https://github.com/OpenVPN/easy-rsa/blob/master/README.quickstart.md
https://easy-rsa.readthedocs.io/en/latest/advanced/

database format (index.txt) description
https://unix.stackexchange.com/questions/569579/what-does-300222061712z-mean-in-openssl-ca-database/569582#569582
```shell
# --batch option
# Expiry days for a new CA
--days=3650 build-ca
# Expiry days for new/renewed certificate.
# eg: '--days=1095 renew server'
easyrsa --req-cn=test.org --subject-alt-name='DNS:example.org,DNS:www.example.org' gen-req test.org nopass
easyrsa sign-req client test1.org
# To copy v3 extensions from request (turned off by default as this is a potential security risk)
easyrsa --copy-ext sign-req client test4.org

# change CA key passphrase
easyrsa set-ec-pass ca
# Remove passphrase from a key
easyrsa set-ec-pass test.org nopass
```
