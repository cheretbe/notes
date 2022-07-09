* https://www.reddit.com/r/homelab/comments/8qlii3/how_do_you_distribute_you_dockers/
* https://www.reddit.com/r/selfhosted/comments/9b4ej2/docker_organizational_best_practices/
* http://blog.thoward37.me/articles/where-are-docker-images-stored/
* Docker build wrapper: https://github.com/rancher/dapper (probably makes no sense - one more dependency, copy is done in dockerfile, no matrix support)
* **A minimal Ubuntu base image modified for Docker-friendliness:** https://github.com/phusion/baseimage-docker
    * Use `phusion/baseimage:master` until [version scheme](https://github.com/phusion/baseimage-docker/issues/543) is changed
* :warning: **Test docker on Raspberry:** https://phoenixnap.com/kb/docker-on-raspberry-pi
    
#### Ansible tests
Possible strategies for Molecule test
* Keep using `geerlingguy/docker-ubuntu1804-ansible` etc. (easiest, but takes time to update packages)
* Rebuild geerlingguy's containers and publish them independently (most logical, but also most work to be done)
    * Will need some kind of automation (in a separate KVM VM, using a scheduled task on AWX. Or creating temporary KVM VM with vagrant?)
    * Set up a scheduled trigger in GitLab CI. Rebuild in two cases;
      * Publishing date is less than `last_updated = $(curl -s -X GET https://hub.docker.com/v2/repositories/geerlingguy/docker-ubuntu2004-ansible/tags/latest | jq .last_updated)
`
      * Some predefined time has passed since last publication
      * https://docs.gitlab.com/ee/ci/pipelines/schedules.html
* Use custom Dockerfile
    * At first glance seems the least appealing. But actually it could be a good compromize. Use `geerlingguy/docker-ubuntu1804-ansible`,
      just adding `apt update`. This needs to be done only once for testing session, then Docker will use local cached image.
    * Check out Molecule's docs/examples on local Dockerfile usage

----
```shell
# Add your user to the docker group
sudo usermod -aG docker $USER

# Run bash in container and delete the container on exit
# Mount a volume (change ro->rw to mount in read-write mode)
#    -v /host/dir:/container/dir:ro
# Forward host's IP port to container
#    --publish=80:8080 
docker run --rm -ti ubuntu:18.04 /bin/bash

docker run -dti --name centos-6 centos:6 /bin/bash
docker exec -ti centos-6 /bin/bash
docker stats [container]

# Run with systemd support and remove on exit
docker run --rm --detach --volume=/sys/fs/cgroup:/sys/fs/cgroup:ro \
  --tmpfs /tmp:exec --tmpfs /run \
  --name centos-8 centos:8 /usr/sbin/init
```
----
https://developers.redhat.com/cheat-sheets/containers/

```shell
# View all containers, running or stopped
docker ps -a

# https://docs.docker.com/config/containers/start-containers-automatically/#use-a-restart-policy
# https://docs.docker.com/engine/reference/commandline/inspect/
# Set restart policy for a container
docker update --restart=always <id or name> [id or name...]
# View current restart policy (this will return just value like "always" on "no")
docker inspect --format "{{ .HostConfig.RestartPolicy.Name }}" <id or name>
# This will return JSON data like '{"Name": "always", "MaximumRetryCount": 0}'
docker inspect --format "{{ json .HostConfig.RestartPolicy }}" <id or name>
# Alternative way to get JSON (package jq needs to be installed)
docker inspect <id or name> | jq .[0] | jq .HostConfig.RestartPolicy

# -d, --detach        Run container in background and print container ID
# -t, --tty           Allocate a pseudo-TTY
# -i, --interactive   Keep STDIN open even if not attached
# -v, --volume list   Bind mount a volume
docker run -v /home/vagrant:/test:rw -d -t -i --name test centos /sbin/init

docker start <id or name>
docker stop <id or name>

# -i, --interactive  Keep STDIN open even if not attached
# -t, --tty          Allocate a pseudo-TTY
docker exec -it <id or name> bash
docker exec -it test yum -y update

# Copy file(s) from/to container
# -L, --follow-link   follow symbolic link
# -a, --archive       archive mode (copy all uid/gid information)
# [!] copies directory trees as well
# [!] the container does not have to be running to use the cp command
docker cp <containerId>:/file/path/within/container /host/path/target
docker cp /host/path/source <containerId>:/file/path/within/container
docker cp -L my_container:/link/to/a/file .

docker rm test
```

### Installation
* https://docs.docker.com/engine/install/ubuntu/
* `docker.io` vs `docker-ce`
    * https://github.com/docker/for-linux/issues/833#issuecomment-549062829
    * https://stackoverflow.com/questions/45023363/what-is-docker-io-in-relation-to-docker-ce-and-docker-ee/57678382#57678382
    * https://www.collabora.com/news-and-blog/blog/2018/07/04/docker-io-debian-package-back-to-life/
```shell
# Tested on Ubuntu 20.04, 22.04

# Install prerequisites
sudo apt install ca-certificates curl gnupg lsb-release

# Add GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
 
# Add repo
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package database
sudo apt update

# Make sure Docker repo is going to be used
apt-cache policy docker-ce

# Install Docker
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# [!!] Don't forget to update /etc/apt/apt.conf.d/50unattended-upgrades

# Execute Docker commands as a non-root user (optional)
# [!] Do not copy/paste as root
sudo usermod -aG docker ${USER}

# Apply new group membership without logging out
su - $USER
id
```

Move `/var/lib/docker/`
```shell
service docker stop
mv /var/lib/docker/* /new/path/docker/
rmdir /var/lib/docker
ln -s /new/path/docker /var/lib/docker
service docker start
```
For ZFS:<br>
Do not move existing data<br>
Edit `/etc/docker/daemon.json` (create if not present)
```json
{
  "storage-driver": "zfs"
}
```

#### Local cache

* https://dev.to/mayeu/saving-time-and-bandwidth-by-caching-docker-images-with-a-local-registry-98b
* https://docs.docker.com/registry/recipes/mirror/

```shell
# as root
mkdir /var/lib/docker-registry

docker run -it --rm registry:2 cat \
       /etc/docker/registry/config.yml > /var/lib/docker-registry/config.yml
       
nano /var/lib/docker-registry/config.yml
```
Add the following to `/var/lib/docker-registry/config.yml`:
```yaml
proxy:
  remoteurl: https://registry-1.docker.io
```
```shell
docker run --restart=always -p 5000:5000 \
         --name v2-mirror -v /var/lib/docker-registry:/var/lib/registry \
         --detach registry:2 serve /var/lib/registry/config.yml
# Check if running (should return empty list)
curl http://localhost:5000/v2/_catalog
```
On a client add the following to `/etc/docker/daemon.json` (create if doesn't exist):
```json
{
    "registry-mirrors": ["http://hostname:5000"]
}
```

```shell
systemctl restart docker

# The info should contain
# Registry Mirrors:
#  http://hostname:5000/
docker info
```
