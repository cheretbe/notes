* https://registry.terraform.io/providers/terra-farm/virtualbox/latest/docs
* https://learn.hashicorp.com/tutorials/terraform/variables?in=terraform/configuration-language
    * https://www.terraform.io/docs/language/values/variables.html
* https://www.digitalocean.com/community/tutorials/how-to-use-ansible-with-terraform-for-configuration-management
* :warning: https://faun.pub/the-best-way-to-structure-your-terraform-projects-3f56b6440dcb
* https://cloud.yandex.ru/docs/solutions/infrastructure-management/terraform-quickstart
    * github search pattern: `yandex-cloud yandex_compute_instance extension:tf`
    * https://registry.terraform.io/providers/yandex-cloud/yandex/latest/docs
    * https://cloud.yandex.ru/docs/compute/pricing
* `.gitignore`: https://github.com/github/gitignore/blob/main/Terraform.gitignore

```shell
terraform init
terraform validate
terraform plan

terraform apply -auto-approve
terraform destroy -auto-approve

terraform taint null_resource.provision && terraform apply -auto-approve
```
