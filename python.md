```python
path = os.path.realpath("/" + path) + ("/" if path.endswith("/") else "")
```

## Code Snippets
Paths
```python
# Join paths
os.path.join(path1, path2)
# Check if file exists
os.path.isfile(fname)
# Normalize path separators
os.path.normpath(fname)
```
## Debugging
```
pip install ipdb
```
```python
import ipdb
ipdb.set_trace()
```
Commands: s(tep), n(ext) - http://frid.github.io/blog/2014/06/05/python-ipdb-cheatsheet/

To review:
* http://chrisstrelioff.ws/sandbox/2016/09/21/python_setup_on_ubuntu_16_04.html

## Installation
### Windows
Download link: https://www.python.org/downloads/windows/
1. Install Python 2.7
    * Install for all users, change installation path to `C:\Python\Python27\`
    * Other than that use default options (make sure "Add python.exe to PATH" is **not** selected)
2. Install Python 3.6
    * Select "Customize installation"
    * Check "Install for all users" and change installation path to `C:\Python\Python36`
    * Check "Add Python to environment variables" (as of 3.6 it defaults to python3)
```bat
:: Install for all users since by default 'c:\users\<user>\appdata\roaming\python\python36\scripts'
:: is not on PATH and 'C:\Python\Python36' is write-accessible without elevation
pip install virtualenvwrapper-win

:: Python3 is default
mkvirtualenv [-p C:\Python\Python27\python.exe] <name>
lsvirtualenv
rmvirtualenv <name>
workon [<name>]

:: Don't use 'setprojectdir .' because hooks don't work for now (v 1.2.1) and there is
:: no way of runnig git commands after entering the project dir (postactivate)
:: Add the following at the end of %USERPROFILE%\Envs\<name>\Scripts\activate.bat instead:
cd <projectdir>
ECHO Checking git repo status...
git fetch --all && git status
```
* http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/
* http://timmyreilly.azurewebsites.net/setup-a-virtualenv-for-python-3-on-windows/
* https://stackoverflow.com/questions/341184/can-i-install-python-3-x-and-2-x-on-the-same-computer

## Linux

Requirements
```bash
pip freeze > requirements.txt
pip install -r requirements.txt

# automatic version update
pip install pur
pur -r requirements.txt
```

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
```bash
mkvirtualenv [-p python3] <name>
lsvirtualenv
rmvirtualenv <name>
workon [<name>]

# Set project directory
cd ~/projects/project-dir
setvirtualenvproject $VIRTUAL_ENV $(pwd)

# Post-activate commands
nano $VIRTUAL_ENV/bin/postactivate
echo Checking git repo status...
git fetch --all && git status
```

Unit tests
```bash
# all tests directories need to have an init.py to be discovered
python -m unittest discover <test_directory>
# -s: directory to start discovery ('.' default)
# -p: pattern to match tests ('test*.py' default)
python -m unittest discover -s <directory> -p '*_test.py'

# pip install pytest
# -v: increase verbosity
# --capture=method: per-test capturing method (one of fd|sys|no)
# -s: shortcut for --capture=no
pytest -v -s
# -k EXPRESSION: only run tests which match the given substring
pytest -k substring
# -m: MARKEXPR: only run tests matching given mark expression
# Use @pytest.mark.mark1 decorator to mark
pytest -m 'mark1 and not mark2'

# pip install nose2
nose2
```

Fix indentation
([!] use file path - by default it scans current directory)
```bash
# Ubuntu
sudo apt install python3.5-examples
sudo apt install python2.7-examples
/usr/share/doc/python3.5/examples/scripts/reindent.py [file.py]
/usr/share/doc/python2.7/examples/Tools/scripts/reindent.py [file.py]
```

Datetime
* http://techblog.thescore.com/2015/11/03/timezones-in-python/
* http://pytz.sourceforge.net/#localized-times-and-date-arithmetic

```python
import dateutil.parser
import dateutil.tz
import pytz
import time

# 2016-12-31T21:25:30+00:30
datetime.datetime(year=2016, month=12, day=31, hour=21, minute=25, second=30, tzinfo=dateutil.tz.tzoffset(None, +1800)).isoformat()

# 2017-01-01T00:55:30+04:00
dateutil.parser.parse("2016-12-31T21:25:30+00:30").astimezone(dateutil.tz.tzoffset(None, 14400)).isoformat()

# 2016-12-31T21:25:30+00:00
pytz.utc.localize(dateutil.parser.parse("2016-12-31T21:25:30")).isoformat()

# tz-aware local UTC time
pytz.utc.localize(datetime.datetime.utcnow())
# tz-aware local time
datetime.datetime.now(dateutil.tz.tzoffset(None, -time.timezone))
# Take DST in account
datetime.datetime.now(dateutil.tz.tzoffset(None, -time.altzone))
```
