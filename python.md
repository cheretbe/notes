To review:
* http://chrisstrelioff.ws/sandbox/2016/09/21/python_setup_on_ubuntu_16_04.html

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
```
mkvirtualenv [-p python3] <name>
lsvirtualenv
rmvirtualenv <name>
workon [<name>]
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
```python
import dateutil.parser
import dateutil.tz
import pytz

# 2016-12-31T21:25:30+00:30
datetime.datetime(year=2016, month=12, day=31, hour=21, minute=25, second=30, tzinfo=dateutil.tz.tzoffset(None, +1800)).isoformat()

# 2017-01-01T00:55:30+04:00
dateutil.parser.parse("2016-12-31T21:25:30+00:30").astimezone(dateutil.tz.tzoffset(None, 14400)).isoformat()

# 2016-12-31T21:25:30+00:00
pytz.utc.localize(dateutil.parser.parse("2016-12-31T21:25:30")).isoformat()
```
