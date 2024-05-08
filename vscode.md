### Default settings

The default settings are hardcoded in the vscode sources. To see all settings in read-only format:<br>
<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>: type `open default settings` (choose **Preferences: Open Default Settings (JSON)**)

### Title bar
* https://dev.to/ismaellopezdev/customize-titlebar-in-vs-code-5hie
* https://marketplace.visualstudio.com/items?itemName=johnpapa.vscode-peacock

<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>: type `open settings` (choose **Preferences:Open User Settings (JSON)**)
```json
"window.title": "${dirty}${activeEditorShort}${separator}${rootName}${separator}${profileName}${separator}${appName}"
```
To view default value and substitute variables descriptions open default settings
