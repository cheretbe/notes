* https://testinfra.readthedocs.io/
* https://github.com/philpep/testinfra
* https://medium.com/@colinwren/configuration-testing-your-docker-containers-with-testinfra-58e79ae85be0
* https://dev.to/koh_sh/using-testinfra-with-ansible-4n7b
* https://opensource.com/article/19/5/using-testinfra-ansible-verify-server-state

```python
import testinfra

def test_os_release(host):
    host_info = host.ansible("setup")["ansible_facts"]["ansible_virtualization_type"]
    print(f"\n########: {host_info}\n")
    # print(host.ansible.get_variables())
    # assert host.file("/etc/os-release").contains("Fedora")
```
