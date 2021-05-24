* https://smallstep.com/docs/step-ca/configuration#basic-x509-template-examples
* https://github.com/smallstep/crypto/blob/master/x509util/templates.go#L98

```shell
STEPDEBUG=1 step ca health
```

```python
cert.extensions.get_extension_for_class(x509.KeyUsage).value
cert.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value._usages
```
