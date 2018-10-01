* https://www.reddit.com/r/homelab/comments/8qlii3/how_do_you_distribute_you_dockers/
* https://www.reddit.com/r/selfhosted/comments/9b4ej2/docker_organizational_best_practices/

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
```
