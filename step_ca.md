* https://github.com/smallstep/cli/releases/latest

```shell
STEPDEBUG=1 step ca health
```

### Offline CA
* https://smallstep.com/docs/step-cli/basic-crypto-operations#run-an-offline-x509-certificate-authority

```shell
mkdir ca-files
mkdir output
step certificate create --profile root-ca "Example Root CA" ./ca-files/root_ca.crt ./ca-files/root_ca.key

step certificate create example.com ./output/example.com.crt ./output/example.com.key \
    --template winrm.tpl --not-after=87600h --insecure --no-password \
    --ca ./ca-files/root_ca.crt --ca-key ./ca-files/root_ca.key
    
# Combine the key and the certificate into a single PKCS12 file with empty password
# https://www.openssl.org/docs/manmaster/man1/openssl.html#Pass-Phrase-Options
openssl pkcs12 -inkey ./output/example.com.key -in ./output/example.com.crt -export -out ./output/example.com.p12 -password pass:
```

`winrm.tpl`:
```
{
    "subject": {{ toJson .Subject }},
    "sans": {{ toJson .SANs }},
    "keyUsage": ["keyEncipherment", "digitalSignature"],
    "extKeyUsage": ["serverAuth"]
}
```

Certificate template files are JSON with [Go language templates](https://golang.org/pkg/text/template/)
and [Sprig](https://github.com/Masterminds/sprig) functions.

* https://smallstep.com/docs/step-ca/configuration#basic-x509-template-examples
* https://github.com/smallstep/crypto/blob/master/x509util/templates.go#L98
