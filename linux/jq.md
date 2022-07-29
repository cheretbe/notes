Convert CSV to JSON
```shell
sudo apt install csvkit

# -H, --no-header-row   Specify that the input CSV file has no header row. Will create default headers (a,b,c,...)
csvjson file.csv > file.json
```

* https://stedolan.github.io/jq/manual/
* https://programminghistorian.org/en/lessons/json-and-jq
* https://jqplay.org/

```bash
last_updated=$(curl -s -X GET https://hub.docker.com/v2/repositories/geerlingguy/docker-ubuntu2004-ansible/tags/latest | jq .last_updated)

# Note the -r option (output raw strings, not JSON texts)
curl -s "https://app.vagrantup.com/api/v1/user/cheretbe" | \
  jq -r '.boxes | sort_by(.name)[] | select(.name|startswith("win10")) | .name'

# |= instead of | passes the values along instead of stripping them
curl -s 'https://app.vagrantup.com/api/v1/user/cheretbe' | \
  jq '.boxes |= map(select((.name|startswith("win10")) and (.updated_at <= "2020-06-29"))) | .boxes[] | [.name, .current_version.version, .updated_at]'

# Note the -c option (compact instead of pretty-printed output)
curl -s 'https://app.vagrantup.com/api/v1/user/cheretbe' | \
  jq -c '.boxes |= map(select((.name|startswith("win10")) and (.updated_at <= "2021-09-20"))) | .boxes | sort_by(.name)[] | [.name, .current_version.version, .updated_at]'

# test(val) test(regex; flags)
# Like match, but does not return match objects, only true or false
curl -s 'https://app.vagrantup.com/api/v1/user/cheretbe' | \
  jq -c '.boxes |= map(select((.name|test("^win10")) and (.updated_at <= "2021-09-20"))) | .boxes | sort_by(.name)[] | [.name, .current_version.version, .updated_at]'
  
# @tsv formats input (must be an array) as TSV (tab-separated values)
curl -s 'https://app.vagrantup.com/api/v1/user/cheretbe' | \
  jq -r '.boxes |= map(select((.name|startswith("win10")) and (.updated_at <= "2021-09-20"))) | .boxes | sort_by(.name)[] | [.name, .current_version.version, .updated_at] | @tsv'
```
