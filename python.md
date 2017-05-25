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
