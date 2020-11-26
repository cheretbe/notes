* https://stedolan.github.io/jq/manual/
* https://programminghistorian.org/en/lessons/json-and-jq
* https://jqplay.org/

```bash
last_updated=$(curl -s -X GET https://hub.docker.com/v2/repositories/geerlingguy/docker-ubuntu2004-ansible/tags/latest | jq .last_updated)
```
