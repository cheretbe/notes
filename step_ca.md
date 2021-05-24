```shell
STEPDEBUG=1 step ca health
```

### Offilne CA
* https://smallstep.com/docs/step-cli/basic-crypto-operations#run-an-offline-x509-certificate-authority

```shell
mkdir ca-files
mkdir output
step certificate create --profile root-ca "Example Root CA" ./ca-files/root_ca.crt ./ca-files/root_ca.key

step certificate create example.com ./output/example.com.crt ./output/example.com.key \
    --template winrm.tpl --not-after=87600h --insecure --no-password \
    --ca ./ca-files/root_ca.crt --ca-key ./ca-files/root_ca.key
```

`winrm.tpl`:
```json
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


```python
cert.extensions.get_extension_for_class(x509.KeyUsage).value
cert.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value._usages
```
