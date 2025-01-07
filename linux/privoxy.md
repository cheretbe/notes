* Built-in URL to view config and docs: http://p.p/
* https://hub.docker.com/r/binhex/arch-privoxyvpn
    * https://github.com/binhex/arch-privoxyvpn/

```shell
docker run \
    --cap-add=NET_ADMIN \
    -p 8118:8118 \
    --name=privoxyvpn \
    -v /root/docker/config:/config \
    -v /etc/localtime:/etc/localtime:ro \
    -e ENABLE_PRIVOXY=yes \
    -e VPN_ENABLED=no \
    binhex/arch-privoxyvpn
```
