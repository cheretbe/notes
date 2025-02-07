```shell
# -s, --silent             Silent mode
# -S, --show-error         Show error even when -s is used
# -L, --location           Follow redirects
# -o, --output <file>      Write to file instead of stdout
# -f, --fail               Fail silently (no output at all) on HTTP errors
# --fail-with-body         (! version 7.76.0+) Fail on HTTP errors but save the body
curl --fail -sSLo file url
```
