* * VB+QEMU: https://github.com/pear2/Net_RouterOS/blob/master/tests/vm/RouterOS.packer.json

```shell
packer build -force -on-error=ask test.pkr.hcl

# Convert from JSON
# To be a valid Packer HCL template, it must have the suffix ".pkr.hcl"
packer hcl2_upgrade -output-file=test.pkr.hcl test.json
```

`test.pkr.hcl` contents (:warning: install `terraform` package in Sublime Text for syntax highlighting)
```hcl
source "vagrant" "build-test" {
  communicator = "ssh"
  provider     = "virtualbox"
  source_path  = "alpine-linux/alpine-x86_64"
}

build {
  sources = ["source.vagrant.build-test"]

  post-processor "shell-local" {
    inline = ["mv output-build-test/package.box output-build-test/custom_box_name.box"]
  }
}
```

```shell
packer build -force -on-error=ask test.json
```

`test.json` contents
```json
{
  "builders": [
    {
      "name": "build-test",
      "communicator": "ssh",
      "source_path": "alpine-linux/alpine-x86_64",
      "provider": "virtualbox",
      "type": "vagrant"
    }
  ],
  "post-processors": [
    {
      "type": "shell-local",
      "inline": ["mv output-build-test/package.box output-build-test/custom_box_name.box"]
    }
  ]
}
```
