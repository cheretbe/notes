```shell
export VAULT_ADDR=https://vault.domain.tld
vault login -method=userpass username=user "password=$MY_VAULT_PASSWORD"
export MY_VAR=$(vault kv get -field=my_var path/to/secrets)
```

* Copy vault data recursively
    * https://github.com/iplabs/vault-cp/tree/master (the script is simple and works, just review carefully)
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

`test.hcl`:
```hcl
storage "file" {
  path    = "./vault/data"
  node_id = "node1"
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = "true"
}

api_addr = "http://127.0.0.1:8200"
```

```shell
vault server -config test.hcl
# Save Unseal Key 1 and Initial Root Token
vault operator init -key-shares=1 -key-threshold=1

vault operator unseal 0000000000000000000000000000000000000000000=
# Creates ~/.vault-token
vault login
```

* https://www.codiwan.com/vault-install-userpass-authentication-secrets-kv-polices-authorization/

`policies/admin.hcl`:
```hcl
path "*" {
    capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
```
`policies/nonadmin.hcl`:
```hcl
 path "servers/*" {
     capabilities = ["list", "read"]
 }
 path "servers/in-east" {
     capabilities = ["list", "read", "update"]
 }
```

```shell
vault secrets enable --path=servers kv
vault policy write admin policies/admin.hcl
vault policy write nonadmin policies/nonadmin.hcl
vault policy list
vault policy read admin

vault write auth/userpass/users/admin password=admin policies=admin
vault write auth/userpass/users/user1 password=user1 policies=nonadmin

vault login -method=userpass username=admin
vault kv put servers/in-east id=in-east location=kolkata
```

* https://github.com/utrace-ltd/postgres-backuper/blob/master/python_pg_backuper.py
* https://github.com/carrier-io/carrier-auth/blob/master/auth/utils/config.py
* https://github.com/rgl/vault-vagrant/blob/master/examples/python/use-postgresql/main.py
* https://github.com/Cloud-42/vault_userpass_util/blob/main/VaultGrabKeyPair.py
* https://github.com/vinayreddy337/vault_examples/blob/main/vault_read.py
* https://github.com/DaviPtrs/vault-user-creator/blob/main/script.py
