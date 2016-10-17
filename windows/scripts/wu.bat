@ECHO OFF

SETLOCAL

SET DoubleClicked=0
FOR %%x IN (%CMDCMDLINE%) DO IF /I "%%~x"=="/C" SET DoubleClicked=1

"%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system" >nul 2>&1
IF ERRORLEVEL 1 (
  ECHO ERROR: Administrative privileges are needed to run this script
  :: White on dark red
  COLOR 4F
  GOTO :EndScript
)

ECHO Checking if required hotfixes are present...


VER | FINDSTR /IL "6.1." > NUL
IF %ERRORLEVEL% EQU 1 GOTO :Win8Check

:: Win7/2008R2
powershell "If ($NULL -eq (Get-Hotfix KB3138612 -ErrorAction SilentlyContinue)) {exit 1} else {exit 0}"
IF ERRORLEVEL 1 (
  ECHO ERROR: Hotfix KB3138612 [Update client march 2016] is not installed
  :: White on dark red
  COLOR 4F
  GOTO :EndScript
)
powershell "If ($NULL -eq (Get-Hotfix KB3172605 -ErrorAction SilentlyContinue)) {exit 1} else {exit 0}"
IF ERRORLEVEL 1 (
  ECHO ERROR: Hotfix KB3172605 [July 2016 update rollup] is not installed
  :: White on dark red
  COLOR 4F
  GOTO :EndScript
)
GOTO :EndHotfixCheck

:Win8Check
VER | FINDSTR /IL "6.3." > NUL
IF %ERRORLEVEL% EQU 1 GOTO :EndHotfixCheck

:: Win8.1/2012R2
powershell "If ($NULL -eq (Get-Hotfix KB3112336 -ErrorAction SilentlyContinue)) {exit 1} else {exit 0}"
IF ERRORLEVEL 1 (
  ECHO ERROR: Hotfix KB3112336 [Update client december 2015] is not installed
  :: White on dark red
  COLOR 4F
  GOTO :EndScript
)

:EndHotfixCheck

IF EXIST "c:\temp\PSWindowsUpdate\PSWindowsUpdate.psm1" GOTO :Skip_Download
  IF NOT EXIST "c:\temp" (
    ECHO Creating 'c:\temp' directory
    MKDIR "c:\temp"
  )
  ECHO Downloading PSWindowsUpdate
  :: https://blogs.iis.net/steveschofield/unzip-several-files-with-powershell
  powershell "(New-Object System.Net.WebClient).DownloadFile('https://go.beercaps.ru/files/util/PSWindowsUpdate.zip', 'c:\temp\PSWindowsUpdate.zip'); [Reflection.Assembly]::LoadWithPartialName('System.IO.Compression.Filesystem'); [System.IO.Compression.ZipFile]::ExtractToDirectory('C:\temp\PSWindowsUpdate.zip', 'C:\temp\')"
  ::powershell "Invoke-WebRequest -Uri 'https://go.beercaps.ru/files/util/PSWindowsUpdate.zip' -OutFile 'c:\temp\PSWindowsUpdate.zip'; Add-Type -AssemblyName 'System.IO.Compression.FileSystem'; [System.IO.Compression.ZipFile]::ExtractToDirectory('C:\temp\PSWindowsUpdate.zip', 'C:\temp\')"

:Skip_Download
ECHO Searching for updates...
powershell -ExecutionPolicy Bypass "If (@(Get-Command Unblock-File*).Count -Eq 0) { Function Unblock-File {} }; Import-Module 'C:\temp\PSWindowsUpdate\PSWindowsUpdate.psm1'; Get-WUInstall -CategoryIDs @('28bc880e-0592-4cbf-8f95-c79b17911d5f', '0fa1201d-4330-4fa8-8ae9-b877473b6441', 'e6cf1350-c01b-414d-a61f-263d14d133b4') -Confirm:$FALSE -NotKBArticleID @('KB890830')"

:EndScript
IF %DoubleClicked%==1 (
  ECHO.
  ECHO ======= Press any key to close this window =======
  PAUSE >NUL
)

ENDLOCAL