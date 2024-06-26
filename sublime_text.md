```shell
 EDITOR='subl -w' ansible-vault edit --vault-password-file vault_file files_to_edit.txt
```

* Multi-selection
   * <kbd>Ctrl</kbd> + <kbd>D</kbd>
   * Skip a match: <kbd>Ctrl</kbd> + <kbd>K</kbd>
       * :warning: It's actually a **3-step** process
       * **1\.** Select with <kbd>Ctrl</kbd> + <kbd>D</kbd> **2.** Mark for skipping with <kbd>Ctrl</kbd> + <kbd>K</kbd> **3.** Press <kbd>Ctrl</kbd> + <kbd>D</kbd> **once again**
   * If you go too far, use <kbd>Ctrl</kbd> + <kbd>U</kbd> (Undo Selection)
* Navigation
   * Goto Symbol: <kbd>Ctrl</kbd> + <kbd>R</kbd>
   * Jump Forward: <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>-</kbd> (minus)
   * Jump Back: <kbd>Alt</kbd> + <kbd>-</kbd> (minus)
   * Goto Definition: <kbd>F12</kbd>
* Find and Replace
   * Use Selection for Find Field: <kbd>Ctrl</kbd> + <kbd>E</kbd>
* Selection
   * (custom, BracketHighlighter) Select text in brackets: <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>B</kbd>
* Editing
   * Join Line Below The Current Line: <kbd>CTRL</kbd> + <kbd>J</kbd>
   * Insert Line Before <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Enter</kbd>
   * Insert Line After <kbd>Ctrl</kbd> + <kbd>Enter</kbd>

------
* Cheat sheet: https://www.cheatography.com/tdeyle/cheat-sheets/sublime-text-3/
* Tips & tricks: https://generalassemb.ly/blog/sublime-text-3-tips-tricks-shortcuts/

Delete previous session
```shell
# Windows location: C:\Users\username\AppData\Roaming\Sublime Text 3\Local
rm ~/.config/sublime-text-3/Local/Session.sublime_session
```

Run from console on Linux
```shell
subl filename
```

Icon in context menu on Windows
```
reg.exe add "HKCR\*\shell\Open with Sublime Text" /v Icon /t REG_SZ /d "c:\Program Files\Sublime Text 3\sublime_text.exe" /f
```
Linux installation
```bash
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt update
sudo apt install sublime-text

# Old unofficial repo
add-apt-repository ppa:webupd8team/sublime-text-3
apt update
apt install sublime-text-installer
```
Settings
```
{
  "show_encoding" : true,
  "show_line_endings": true,
  "draw_white_space": "all",
  "rulers": [80],
  "tab_size": 2,
  "translate_tabs_to_spaces": true,
  "highlight_modified_tabs": true,
  "remember_open_files": false,
  "hot_exit": false,
  "show_project_first": true,
  "auto_complete": false,
  "bold_folder_labels": true,
  "highlight_line": true,
  "indent_guide_options":
    [
      "draw_normal",
      "draw_active"
    ]
}
```
On linux:
```
  "font_face": "Consolas",
  "line_padding_bottom": 2,
  "line_padding_top": 2
```
File exclusion patterns
```yaml
# default for ST 4
"file_exclude_patterns": ["*.pyc", "*.pyo", "*.exe", "*.dll", "*.obj","*.o", "*.a", "*.lib", "*.so", "*.dylib", "*.ncb", "*.sdf", "*.suo", "*.pdb", "*.idb", ".DS_Store", ".directory", "desktop.ini", "*.class", "*.psd", "*.db", "*.sublime-workspace"],
```
Custom tab size for python files: `Preferences > Settings-Syntax Specific`
```
{
  # File name should be something like "Python.sublime-settings"
  "tab_size": 4
}
```

Set syntax highlighting for files with extensions:<br>
`View` -> `Syntax` -> `Open all with current extension as ...`

Custom code page for Windows files (`Preferences > Settings-Syntax Specific`). :warning: `default_encoding` doesn't work for some reason
```
{
  # .ps1 files
  "fallback_encoding": "Cyrillic (Windows 1251)"
  # .bat files
  "fallback_encoding": "Cyrillic (Windows 866)"
}
```

Colors
* Color picker: https://www.w3schools.com/colors/colors_picker.asp
* Less usable, but has text on background preview: https://www.wincalendar.com/Color-Picker
* Theme editor (use `Gallery` button to view list): https://tmtheme-editor.herokuapp.com/#!/editor/theme/Monokai
* :warning: Contrast checker: https://webaim.org/resources/contrastchecker/
* In ST4 default color scheme is _Mariana_ instead of _Molokai_
* Default color scheme definitions are in `/opt/sublime_text/Packages/Color Scheme - Default.sublime-package` (.zip file)

`Preferences` > `Customize Color Scheme`:
```json
# Mariana theme customization
{
  "variables":
  {
  },
  "globals":
  {
    "selection": "#5A647EE0"
  },
  "rules":
  [
    
  ]
}
```

```json
# Molokai theme customization
{
  "variables":
  {
  },
  "globals":
  {
    "selection": "#25375b",
    "active_guide": "hsl(180, 36%, 54%)",
    "stack_guide": "hsl(180, 36%, 54%)",
    "guide": "color(hsl(180, 36%, 54%) alpha(0.4))"
  },
  "rules":
  [
  {
      "name": "Comment",
      "scope": "comment, punctuation.definition.comment",
      "foreground": "#6e8bc4"
  }
  ]
}
```

Linters
* <kbd>Ctl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> > "Install Packages" > "SublimeLinter"
* pylint
  * Install pylint system-wide (for example with `pip3 install pylint` as root)
  * <kbd>Ctl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> > "Install Packages" > SublimeLinter-pylint

`~/.pylintrc` example:
```
[MESSAGES CONTROL]

disable=missing-module-docstring,
        missing-function-docstring
```
```json
  "pylinter":
  {
    "python_bin": "/home/user/.cache/venv/py3"
  }
```

Printing. Not implemented and is not going to be at least in ST3. Workaround: http://facelessuser.github.io/ExportHtml/<br>
Install package `ExportHtml`. For export use <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> and look for `Export HTML: Show Export Menu`. It does actual export, not enables some export menu in ST :)

"Open With" on Ubuntu: http://askubuntu.com/questions/732464/sublime-text-not-showing-in-nautilus-open-with-menu/755041#755041

Clear stuck auto-open of no longer existing file on startup: remove `~/.config/sublime-text-3/Local/Session.sublime_session` (also clears windows position, minimap setting, etc.)

Packages:
Install [Package Control](https://packagecontrol.io/installation#st3)

**CTRL-SHIFT-P**, "Package Control: Install Package"
* :heavy_check_mark: SideBarEnhancements
* :question: `Monokai JSON+` (then add `"color_scheme": "Packages/Monokai JSON+/Monokai JSON+.tmTheme"` to `Preferences` > `Settings - Syntax Specific` )
* :question: `Theme - Soda` (then add `"theme": "Soda Dark 3.sublime-theme"` to "Settings - User")
* :question: `GitGutter`
* :heavy_check_mark: `Powershell`: https://packagecontrol.io/packages/PowerShell
* :question: `SublimeBookmarks`: https://packagecontrol.io/packages/Sublime%20Bookmarks
* :heavy_check_mark: `BracketHighlighter`: http://facelessuser.github.io/BracketHighlighter/

BracketHighlighter config  (`Preferences` > `Package Settings` > `BracketHighlighter` > `Bracket Setting`)<br>
Add to settings
```
    "match_brackets": false,
    "match_brackets_angle": false,
    "match_brackets_braces": false,
    "match_brackets_content": false,
    "match_brackets_square": false,
    "match_tags": false
```
~~Keybindings (`Preferences` > `Key Bindings`):~~<br>
`Preferences` > `Package Settings` > `BracketHighlighter` > `Key Bindings - User`:
```
// Select text between brackets
{
    "no_outside_adj": null,
    "keys": ["ctrl+shift+b"],
    "command": "bh_key",
    "args":
    {
        "lines" : true,
        "plugin":
        {
            "type": ["__all__"],
            "command": "bh_modules.bracketselect"
        }
    }
}
```
Other examples: https://github.com/facelessuser/BracketHighlighter/blob/master/Example.sublime-keymap
