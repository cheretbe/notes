```batch
mkdir python\x64\
mkdir python\x86\
mkdir python\packages
```
* Download embeddable packages from https://www.python.org/downloads/windows/
* :warning: Add custom `../packages` entry to both `lib\python\x64\python39._pth` and `lib\python\x64\python39._pth`
* Initial pip installation
    * download https://bootstrap.pypa.io/get-pip.py
    * run `python\x64\python.exe get-pip.py` (this will create `python\x64\Lib` and `python\x64\Scripts` directories)
    * copy `python\x64\Lib\site-packages` contents to `python\packages`
    * make sure `python\packages` contains `.gitignore` file with the following entry: `__pycache__/`
    * now pip could be run like this: `python\x64\python.exe -m pip`
    * remove `python\x64\Lib` and `python\x64\Scripts`

```batch
:: Install/upgrade additional packages
python\x64\python.exe -m pip install --upgrade -t python\packages -r requirements.txt
```
