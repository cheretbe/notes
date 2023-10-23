* https://resources.rundeck.com/plugins/http-notification-plugin/
    * https://github.com/rundeck-plugins/http-notification/releases
 
### Key Storage

`Project Settings` > `Key Storage`

* Select its storage path (e.g. `keys/project/project-name/key-name`)

### Nodes

`/home/rundeck/server/data/project_name_nodes.yml`

```yaml
host.domain.tld:
  nodename: host.domain.tld
  hostname: host.domain.tld
  ssh-key-storage-path: keys/project/project-name/key-name
  description: Host description
  username: rundeck-user-name
  tags: ''
```
