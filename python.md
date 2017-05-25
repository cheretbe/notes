To review:
* http://chrisstrelioff.ws/sandbox/2016/09/21/python_setup_on_ubuntu_16_04.html

```bash
sudo su -
wget "https://bootstrap.pypa.io/get-pip.py"
python get-pip.py
pip install virtualenv
```
Virtualenv

```bash
# Python 2
virtualenv newenv
# Python 3
virtualenv -p python3 newenv
source newenv/bin/activate
deactivate
```


Virtualenvwrapper

* http://virtualenvwrapper.readthedocs.io/en/latest/install.html

```bash
sudo apt install build-essential python-dev python3-dev python-pip python3-pip
pip install --user virtualenvwrapper
```
add the following to `~/.bashrc`
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/projects
source $HOME/.local/bin/virtualenvwrapper.sh
```
Restart shell of run
```bash
source ~/.bashrc
```
Essential commands:
```
mkvirtualenv <name>
lsvirtualenv
rmvirtualenv <name>
workon [<name>]
```
