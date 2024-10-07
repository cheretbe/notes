### Default settings

The default settings are hardcoded in the vscode sources. To see all settings in read-only format:<br>
<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>: type `open default settings` (choose **Preferences: Open Default Settings (JSON)**)

### Title bar
* https://dev.to/ismaellopezdev/customize-titlebar-in-vs-code-5hie
* :point_right: Change workspace color: https://marketplace.visualstudio.com/items?itemName=johnpapa.vscode-peacock

<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>: type `open settings` (choose **Preferences:Open User Settings (JSON)**)
```json
# Root name first
"window.title": "${dirty}${rootName}${separator}${activeEditorShort}${separator}${profileName}${separator}${appName}"
```
To view default value and substitute variables descriptions open [default settings](#default-settings).

### Extensions
* https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph
* https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens

### Indent on pasting

* [editor.formatOnPaste](https://stackoverflow.com/questions/41790069/settings-to-copy-paste-with-correct-indentation-in-visual-studio-code/45359863#45359863) does too much (also auto-formats pasted code)
* Use this: https://marketplace.visualstudio.com/items?itemName=Rubymaniac.vscode-paste-and-indent
* Hints
    * to open `keybindings.json` go to `File` > `Preferences` > `Keyboard Shortcuts` and then click a button in the tab-bar (top right corner)
    * <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>: type `open settings` (choose **Preferences:Open User Settings (JSON)**)

keybindings.json
```json
    {
        "key": "ctrl+shift+v",
        "command": "extension.paste-and-indent",
        "when": "editorTextFocus && !editorReadonly"
    }
```
settings.json (doesn't work)
```json
{
    "pasteAndIndent.selectAfter": true
}
```
