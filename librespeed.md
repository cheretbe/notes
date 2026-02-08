## Self-hosted [speedtest](https://www.speedtest.net/) alternative

* https://github.com/librespeed/speedtest

### CLI

* https://github.com/librespeed/speedtest-cli

```shell
# List public servers
curl https://librespeed.org/backend-servers/servers.php | jq

# Specify a server without upload/download tests (ping only)
./librespeed-cli --server 87 --no-download --no-upload

# https://github.com/librespeed/speedtest-cli/issues/83
# https://pkg.go.dev/net/http#ProxyFromEnvironment
# Looks like ALL_PROXY is not supported (and doesn't work in 1.0.12)
HTTPS_PROXY=socks5://localhost:1080 ./librespeed-cli --server 87
```
