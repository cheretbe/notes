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
