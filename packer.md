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
