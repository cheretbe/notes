* https://cloud.yandex.ru/docs/cli/quickstart
* https://cloud.yandex.ru/ru/docs/compute/concepts/vm-platforms
* https://cloud.yandex.ru/ru/docs/compute/pricing#prices-instance-resources

```shell
yc config profile create test
yc config profile activate test
yc init --federation-id=00000000000000000000

# https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token
# Срок жизни OAuth-токена 1 год. После этого необходимо получить новый OAuth-токен и повторить процедуру аутентификации
yc init

yc compute instance list --folder-id=00000000000000000000 --format json |
  jq -r '. | sort_by(.name)[] | (.name) + "  ansible_host=" + .network_interfaces[0].primary_v4_address.address'

yc compute image list --folder-id standard-images
yc compute image list --folder-id standard-images --format json | jq -r '[.[] | select(.family == "ubuntu-2204-lts")] | sort_by(.created_at)[-1].id'
yc compute image list --folder-id standard-images --format json | jq -r '[.[] | select(.family == "ubuntu-2204-lts")] | sort_by(.created_at)[-1] | .id + " " + .name + " created at: " + .created_at'

yc vpc subnet list

# [!!] user name is ya-cloud
yc compute instance create \
    --name docker-test \
    --zone ru-central1-b \
    --network-interface subnet-name=default-ru-central1-b,nat-ip-version=ipv4 \
    --platform standard-v3 \
    --preemptible \
    --core-fraction 50 \
    --memory 2 \
    --cores 2 \
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2204-lts,type=network-ssd,size=15 \
    --ssh-key ~/.ssh/id_ed25519.pub

yc compute instance delete --name docker-test
```
