Unsorted
```python
path = os.path.realpath("/" + path) + ("/" if path.endswith("/") else "")
```
* https://anthony-tuininga.github.io/cx_Freeze/
    * https://ptmccarthy.github.io/2016/01/22/python-cx-freeze/
* https://github.com/squeaky-pl/portable-pypy
* https://docs.python.org/3/distutils/sourcedist.html
* https://github.com/pypa/pip/issues/4207#issuecomment-281236055 (+ `pip install -t`)

Git ignore
```
.cache/
__pycache__/
*.pyc
```

# Table of Contents
* [Code Snippets](#code-snippets)
* [Debugging](#debugging)
* [Installation](#installation)
    * [Windows](#windows)
    * [Linux](#linux)
* [Requirements](#requirements)
* [Unit Tests](#unit-tests)
* [Fix Indentation](#fix-indentation)

## Code Snippets
* Unit tests
    * [unittests_examples.py](files/python/unittests_examples.py)
    * [test_unittests_examples.py](files/python/test_unittests_examples.py)
```python
#!/usr/bin/env python

with open("filename", "w") as f:
    f.write("test")

# Join paths
os.path.join(path1, path2)
# Check if file exists
os.path.isfile(fname)
# Normalize path separators
os.path.normpath(fname)
# Script dir
os.path.dirname(os.path.realpath(__file__))

# Remove a file
os.remove(path)
# Remove an empty directory
os.rmdir(path)
# Remove directories recursively (does not work?)
os.removedirs(name)
# Use this instead
shutil.rmtree(path)

# Get current temp directory
import tempfile
tempfile.gettempdir()
f = tempfile.NamedTemporaryFile(delete=False)
f.close()

# Create a directory
# [!] May cause a race condition in a multi-process evironment
if not os.path.exists(directory):
    os.makedirs(directory)
# Python 3.2+
os.makedirs(directory, exist_ok=True)
# Python 2.5+
try:
    os.makedirs(directory)
except OSError as exc:  # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(directory):
        pass
    else:
        raise
# https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
# https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python

# Run external process
import subprocess
# check_call either returns 0 or throws an exception
subprocess.check_call(("ls", "-lh", "."))
# expand ~
import os
subprocess.check_call(("cat", os.path.expanduser("~/path/to/a/file")))
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

# Current time as ISO 8601 string with TZ offset an no microseconds
datetime.datetime.now(dateutil.tz.tzoffset(None, -time.altzone)).replace(microsecond=0).isoformat()

# tz-aware local UTC time
pytz.utc.localize(datetime.datetime.utcnow())
# tz-aware local time
datetime.datetime.now(dateutil.tz.tzoffset(None, -time.timezone))
# Take DST in account
datetime.datetime.now(dateutil.tz.tzoffset(None, -time.altzone))

# Print localized datetime
import locale
locale.setlocale(locale.LC_ALL, '')
datetime.datetime.now().strftime("%x %X")

# Timedelta
datetime.timedelta(seconds=333)
# Elapsed time
start = time.time()
print(str(datetime.timedelta(seconds=round(time.time() - start))))
```

* [\[ TOC \]](#table-of-contents)

## Debugging
```
pip install ipdb
```
```python
import ipdb
ipdb.set_trace()
```
Commands: s(tep), n(ext), p expression, c(ont(inue)) - http://frid.github.io/blog/2014/06/05/python-ipdb-cheatsheet/

```python
// Inspect variable
from pprint import pprint
pprint(vars(os.environ))
type(os.environ)
import inspect
pprint(inspect.getmembers(os._Environ))
# cls’s base classes
pprint(inspect.getmro(os._Environ))
```
* [\[ TOC \]](#table-of-contents)

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
-----
* [\[ TOC \]](#table-of-contents)

### Linux

To review:
* http://chrisstrelioff.ws/sandbox/2016/09/21/python_setup_on_ubuntu_16_04.html

```shell
# As root
apt install python-pip
# As user
pip install --user --upgrade pip
pip install --user virtualenvwrapper

# On server .local/bin might not be on PATH when .bashrc is loaded
# export PATH=~/.local/bin:$PATH
# source $HOME/.local/bin/virtualenvwrapper.sh
source virtualenvwrapper.sh

# Make settings permanent
cat >>~/.bashrc <<EOL

# Initialize Virtualenvwrapper
source virtualenvwrapper.sh
EOL

# Most likely Python 2 is default
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
* [\[ TOC \]](#table-of-contents)

## Requirements
```bash
pip freeze > requirements.txt
pip install -r requirements.txt

# automatic version update
pip install pur
pur -r requirements.txt
```
`requirements.txt` example
```
pyreadline; sys_platform == 'win32'
atomac==1.1.0; sys_platform == 'darwin'
futures>=3.0.5; python_version < '3.0'
futures>=3.0.5; python_version == '2.6' or python_version=='2.7'
```
* http://pip.readthedocs.io/en/stable/user_guide/#requirements-files
* https://stackoverflow.com/questions/41457612/how-to-use-requirements-txt-to-install-all-dependencies-in-a-python-project
-----
* [\[ TOC \]](#table-of-contents)

## Unit tests
* [unittests_examples.py](files/python/unittests_examples.py)
* [test_unittests_examples.py](files/python/test_unittests_examples.py)

Unsorted
```
Reset the call history of a mock function
func_mock.reset_mock()
```

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
* [\[ TOC \]](#table-of-contents)

## Fix indentation
[!] use file path - by default it scans current directory
```bash
# Ubuntu
sudo apt install python3.5-examples
sudo apt install python2.7-examples
/usr/share/doc/python3.5/examples/scripts/reindent.py [file.py]
/usr/share/doc/python2.7/examples/Tools/scripts/reindent.py [file.py]
```
* [\[ TOC \]](#table-of-contents)
