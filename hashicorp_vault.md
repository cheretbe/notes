* Downloads: https://www.vaultproject.io/downloads

```shell
export VAULT_ADDR='http://127.0.0.1:8200'
vault status
# or
vault status -address=http://localhost:8200 -format=json
```

```shell
vault auth list

# Enables userpass at 'userpass/'
vault auth enable userpass
# Enables userpass at 'my-auth/'
vault auth enable -path=my-auth userpass
# or
vault write sys/auth/my-auth type=userpass
```

* https://github.com/utrace-ltd/postgres-backuper/blob/master/python_pg_backuper.py
* https://github.com/carrier-io/carrier-auth/blob/master/auth/utils/config.py
* https://github.com/rgl/vault-vagrant/blob/master/examples/python/use-postgresql/main.py
* https://github.com/Cloud-42/vault_userpass_util/blob/main/VaultGrabKeyPair.py
* https://github.com/vinayreddy337/vault_examples/blob/main/vault_read.py
* https://github.com/DaviPtrs/vault-user-creator/blob/main/script.py
