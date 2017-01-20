Ubuntu 16.04, GitLab 8

https://about.gitlab.com/downloads/

Install packages
```shell
# Prerequisites
sudo apt-get install curl openssh-server ca-certificates postfix
# Add repository and install the package
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
sudo apt-get install gitlab-ce
```

To store git data in and alternative directory adjust `git_data_dir` parameter in `/etc/gitlab/gitlab.rb`
```
git_data_dir "/var/opt/gitlab/git-data"
```
https://gitlab.com/gitlab-org/omnibus-gitlab/blob/629def0a7a26e7c2326566f0758d4a27857b52a3/README.md#storing-git-data-in-an-alternative-directory

Configure and start GitLab
```
sudo gitlab-ctl reconfigure
```
Visit server URL in a web browser and set password for the user `root`
