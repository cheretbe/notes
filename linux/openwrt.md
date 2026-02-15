```shell
nmcli con show | grep -i ether
CONNECTION_UUID="connection-uuid"
nmcli connection modify $CONNECTION_UUID ipv4.route-metric 700
nmcli connection down $CONNECTION_UUID
nmcli connection up $CONNECTION_UUID

```
