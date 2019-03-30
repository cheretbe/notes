* https://www.reddit.com/r/homelab/comments/8qlii3/how_do_you_distribute_you_dockers/
* https://www.reddit.com/r/selfhosted/comments/9b4ej2/docker_organizational_best_practices/
* http://blog.thoward37.me/articles/where-are-docker-images-stored/
----
```shell
docker run -dti --name centos-6 centos:6 /bin/bash
docker exec -ti centos-6 /bin/bash
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

docker rm test
```

Installation (18.04)
```shell
# Install prerequisites
sudo apt install apt-transport-https ca-certificates curl software-properties-common
# Add GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# Add repo
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
# Update package database
sudo apt update
# Make sure Docker repo is going to be used
apt-cache policy docker-ce
# Install Docker
sudo apt install docker-ce

# [!!] Don't forget to update /etc/apt/apt.conf.d/50unattended-upgrades

# Execute Docker commands as a non-root user (optional)
# [!] Do not copy/paste as root
sudo usermod -aG docker ${USER}
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
