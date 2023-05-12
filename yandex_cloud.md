* https://cloud.yandex.ru/docs/cli/quickstart

```shell
yc config profile create test
yc config profile activate test
yc init --federation-id=00000000000000000000

yc compute instance list --folder-id=00000000000000000000 --format json |
  jq -r '. | sort_by(.name)[] | (.name) + "  ansible_host=" + .network_interfaces[0].primary_v4_address.address'
```
