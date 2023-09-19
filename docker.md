* :warning: 2check https://github.com/sickcodes/Docker-OSX
* https://www.reddit.com/r/homelab/comments/8qlii3/how_do_you_distribute_you_dockers/
* https://www.reddit.com/r/selfhosted/comments/9b4ej2/docker_organizational_best_practices/
* http://blog.thoward37.me/articles/where-are-docker-images-stored/
* Docker build wrapper: https://github.com/rancher/dapper (probably makes no sense - one more dependency, copy is done in dockerfile, no matrix support)
* **A minimal Ubuntu base image modified for Docker-friendliness:** https://github.com/phusion/baseimage-docker
    * Use `phusion/baseimage:master` until [version scheme](https://github.com/phusion/baseimage-docker/issues/543) is changed
* :warning: **Test docker on Raspberry:** https://phoenixnap.com/kb/docker-on-raspberry-pi
* What is the difference between CMD and ENTRYPOINT in a Dockerfile? https://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile
* **iptables** settings: https://github.com/cheretbe/notes/blob/master/linux/networking.md#docker
* https://www.googlinux.com/how-to-list-all-tags-of-a-docker-image/

```shell
# Remove -f to see what's going to be deleted (example below)
#   - all stopped containers
#   - all networks not used by at least one container
#   - all images without at least one container associated to them
#   - all build cache
docker system prune -af

# Also remove -f to see a warning
# This will remove all local volumes not used by at least one container
docker volume prune -f
```

```shell
curl https://registry.hub.docker.com/v2/repositories/library/mariadb/tags/ | jq '.results[]["name"]'
curl https://registry.hub.docker.com/v2/repositories/library/mariadb/tags/?page=2 | jq '.results[]["name"]'

i=0
while [ $? == 0 ]
do 
   i=$((i+1))
   curl https://registry.hub.docker.com/v2/repositories/library/debian/tags/?page=$i 2>/dev/null|jq '."results"[]["name"]'
done
```

```shell
# Check if image exists locally
docker images myimage
docker image inspect node:latest
```
### skopeo
* https://github.com/containers/skopeo
* https://github.com/cheretbe/docker-configs/blob/main/seafile/README.md#version-upgrade
```shell
docker run --rm -it alpine:latest
apk add skopeo jq

skopeo list-tags docker://python
skopeo list-tags docker://gitlab/gitlab-ce | grep 16.0.7
# View digest
skopeo inspect docker://gitlab/gitlab-ce:16.0.7-ce.0 | jq '.Digest'
```


### Configuration

#### Move /var/lib/docker/
Option 1<br>
Edit `/etc/docker/daemon.json`, create if doesn't exist
```json
{
    "data-root": "/mnt/docker",
    "storage-driver": "overlay2"
}
```
```shell
systemctl stop docker
# note the trailing slash in the source path
rsync -avxP /var/lib/docker/ /mnt/docker
cd /var/lib
mv docker/ docker.bak/
systemctl start docker
# Make sure there is only docker.bak
ls -lha | grep docker
# Should return "overlay2"
docker info | grep 'Storage Driver:'
# Check if everything is ok before deleting
rm -rf docker.bak/
```


Option 2 (ugly)
```shell
service docker stop
mv /var/lib/docker/* /new/path/docker/
rmdir /var/lib/docker
ln -s /new/path/docker /var/lib/docker
service docker start
```

Option 3 (not tested):

Stop the Docker service. Directly mount a filesystem (ext4, xfs with d_type true flag!) into /var/lib/docker from /etc/fstab or mount it somehwere else and bend the data-root configuration in /etc/docker/daemon.json (the file might not exist yet). Then restart the Docker service again.

Check the output of docker info | grep 'Storage Driver:' to see which storagedriver is used. On wrong formated xfs, this will fall back to device mapper. If the command returs “overlay2” everything is fine. If it says “device mapper” make sure to figure out why and remedy that problem.

For ZFS (left for the reference, most likely is not worth using):<br>
Do not move existing data<br>
Edit `/etc/docker/daemon.json` (create if not present)
```json
{
  "storage-driver": "zfs"
}
```


#### Miscellaneous

`/etc/docker/daemon.json` (create if doesn't exist)
```json
{
    "max-concurrent-uploads": 1,
    "max-concurrent-downloads": 1
}
```
`systemctl restart docker.service`

### Memory settings

* :warning::warning: kernel settings: https://github.com/cheretbe/notes/blob/master/linux/swap.md#limiting-swap-for-containers
* https://docs.docker.com/config/containers/resource_constraints/
    * https://docs.docker.com/config/containers/resource_constraints/#--memory-swap-details 
    * If --memory-swap is set to 0, the setting is ignored, and the value is treated as unset
    * If --memory="300m" and --memory-swap="1g", the container can use 300m of memory and 700m (1g - 300m) swap 
    * Prevent a container from using swap (set memswap_limit to the same value as mem_limit)
    ```
        mem_limit: 128m
        memswap_limit: 128m
    ```
    
View current memory settings for a container
```shell
docker inspect -f '{{ .HostConfig.Memory }}' container-name
docker inspect -f '{{ .HostConfig.MemorySwap }}' container-name
docker inspect -f '{{ index .Config.Labels "com.docker.compose.project.config_files" }}' container-name
```

### Docker Compose

* Samples: https://docs.docker.com/samples/
    * Awesome Compose: https://github.com/docker/awesome-compose
    * Docker Samples: https://github.com/dockersamples?q=&type=all&language=&sort=stargazers
* Directory structure example: https://github.com/rundeck/docker-zoo
* GitLab with a runner example: https://www.czerniga.it/2021/11/14/how-to-install-gitlab-using-docker-compose/
* https://runnable.com/docker/advanced-docker-compose-configuration

```shell
# Update container images
docker compose up --force-recreate --build -d
# Update (rebuild) specific containers (services) instead of all
# https://docs.docker.com/engine/reference/commandline/compose_up/
# Without one or more service_name arguments all images will be built
# if missing and all containers will be recreated
docker compose up --force-recreate --build -d service_name_1 service_name_2
# Consider a cleanup after that
docker image prune -f

# Stops the containers
docker-compose stop
# Stops and removes the containers
docker compose down

docker compose ls --all
```
    
### Ansible tests
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
# Remove all (!) containers
docker ps -a -q | xargs docker rm

# List mounted volumes for a container
docker inspect -f '{{ .Mounts }}' containerid

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

# Applynew group membership without logging out
su - $USER
id
```

#### Caching proxy

* https://github.com/rpardini/docker-registry-proxy
* https://github.com/cheretbe/docker-configs/tree/main/docker-registry-proxy
* https://github.com/cheretbe/ansible-playbooks/blob/master/docker-ce/tasks/main.yml#L99

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
### Minikube
With driver none
```shell
# install docker-ce

sudo apt install conntrack

curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
# or
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl


curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube
sudo install minikube /usr/local/bin/

# [!!!] Run these commands as root
wget https://storage.googleapis.com/golang/getgo/installer_linux
chmod +x ./installer_linux
./installer_linux
source ~/.bash_profile

git clone https://github.com/Mirantis/cri-dockerd.git
cd cri-dockerd
mkdir bin
go build -o bin/cri-dockerd
mkdir -p /usr/local/bin
install -o root -g root -m 0755 bin/cri-dockerd /usr/local/bin/cri-dockerd
cp -a packaging/systemd/* /etc/systemd/system
sed -i -e 's,/usr/bin/cri-dockerd,/usr/local/bin/cri-dockerd,' /etc/systemd/system/cri-docker.service
systemctl daemon-reload
systemctl enable cri-docker.service
systemctl enable --now cri-docker.socket

# [!] Non-root again
VERSION="v1.26.0" # check latest version in /releases page
wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
sudo tar zxvf crictl-$VERSION-linux-amd64.tar.gz -C /usr/local/bin
rm -f crictl-$VERSION-linux-amd64.tar.gz

minikube start --vm-driver=none
minikube status
```
