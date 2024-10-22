* https://registry.terraform.io/providers/terra-farm/virtualbox/latest/docs
* https://learn.hashicorp.com/tutorials/terraform/variables?in=terraform/configuration-language
    * https://www.terraform.io/docs/language/values/variables.html
* https://www.digitalocean.com/community/tutorials/how-to-use-ansible-with-terraform-for-configuration-management
* :warning: https://faun.pub/the-best-way-to-structure-your-terraform-projects-3f56b6440dcb
    * https://medium.com/codex/terraform-best-practices-how-to-structure-your-terraform-projects-b5b050eab554
* https://cloud.yandex.ru/docs/solutions/infrastructure-management/terraform-quickstart
    * github search pattern: `yandex-cloud yandex_compute_instance extension:tf`
    * https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs
    * https://cloud.yandex.ru/docs/compute/pricing
* `.gitignore`: https://github.com/github/gitignore/blob/main/Terraform.gitignore

```shell
terraform init
terraform validate
terraform plan

# list resources in the state (without properties)
terraform state list
# remove a resource from state
terraform state rm <name>

terraform apply -auto-approve
terraform destroy -auto-approve

terraform taint null_resource.provision && terraform apply -auto-approve

# Move to local backend
# Make a backup of current state just in case
terraform state pull > ~/temp/backup.tfstate
# Comment out the backend block and reinit
terraform init -migrate-state
# Check that there is no changes
terraform plan
```

```tf
# External datasource example
# [!] Even though the doc for external datasource states that "program must then
#     produce a valid JSON object on stdout", it actually supports only limited
#     subset of JSON (no arrays etc.). That's why jq is used here
#     See:
#     https://github.com/hashicorp/terraform/issues/12249
#     https://github.com/hashicorp/terraform/issues/12256
data "external" "server_mac" {
  depends_on=[module.ovpn_server_user]

  program = [
    "bash", "-c",
    "docker inspect -f '{{json .NetworkSettings.Networks.terraform_ovpn_network}}' terraform-docker-ovpn-server | jq  -j '{mac_addr: .MacAddress}'"
  ]
}
```

```shell
# Dump state from Consul
curl --silent --fail --header "X-Consul-Token: $CONSUL_HTTP_TOKEN" -X GET \
  https://consul.domain.tld/v1/kv/projects/project_name/terraform_prod.tfstate | \
  jq -r '.[].Value' | base64 -d

```

### Debugging

```shell
# Debug single external resource
terraform apply -target=data.external.current_user_name
terraform show
```

#### templatefile() function
```hcl
# Add temporary local resource
locals {
  dummy = templatefile("${path.module}/template.yml.tftpl", {var_name = var.value})
}
```
```shell
terraform apply -target=locals.dummy && echo "local.dummy" | terraform console
```
#### template_file
```shell
# Template debugging
terraform apply -target=data.template_file.example
echo "data.template_file.example.rendered" | terraform console
# or
terraform state show template_file.example
```
