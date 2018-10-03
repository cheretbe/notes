* https://www.reddit.com/r/homelab/comments/8qlii3/how_do_you_distribute_you_dockers/
* https://www.reddit.com/r/selfhosted/comments/9b4ej2/docker_organizational_best_practices/
* http://blog.thoward37.me/articles/where-are-docker-images-stored/

```shell
# View all containers, running or stopped
docker ps -a

docker start <id or name>
docker stop <id or name>
docker exec -it <id or name> bash
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
