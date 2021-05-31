* Download embeddable packages from https://www.python.org/downloads/windows/ and extract to `python\x64` and `python\x86`
* Add custom `../packages` entry to both `python\x64\python39._pth` and `python\x86\python39._pth`
* Initial pip installation
    * download https://bootstrap.pypa.io/get-pip.py: `powershell "wget https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"`
    * run `python\x64\python.exe get-pip.py` (this will create `python\x64\Lib` and `python\x64\Scripts` directories)
    * copy `python\x64\Lib\site-packages` contents to `python\packages`: `xcopy python\x64\Lib\site-packages python\packages\ /E`
    * make sure `python\packages` contains `.gitignore` file with the following entry: `__pycache__/`
    * now pip could be run like this: `python\x64\python.exe -m pip`
    * `DEL get-pip.py & RMDIR /S /Q python\x64\Lib & RMDIR /S /Q python\x64\Scripts`

```batch
:: Install/upgrade additional packages
python\x64\python.exe -m pip install --upgrade -t python\packages -r requirements.txt
```

Batch wrapper example (`test.bat`)
```batch
@ECHO OFF

SETLOCAL

IF "%ProgramFiles(x86)%"=="" (SET CPUArch=x86) ELSE (SET CPUArch=x64)
"%~dp0python\%CPUArch%\python.exe" "%~dp0test.py" %*

ENDLOCAL
```
