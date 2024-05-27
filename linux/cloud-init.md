* logs are in `/var/log/cloud-init.log`
* some data (?) are in `/var/lib/cloud`

`preserve_sources_list` gotcha:
```yaml
# 'preserve_sources_list' repeated twice is intentional. There is a bug in cloud-init where it tries to
# reconcile the two settings as if they're different and fails with the following error:
#   Old and New apt format defined with unequal values False vs True @ apt_preserve_sources_list
# So we can't just use newer 'apt: {preserve_sources_list: true}' setting
apt_preserve_sources_list: true
apt:
  preserve_sources_list: true

```
