By default it loads `%userprofile%\Documents\AutoHotkey.ahk` file

```
; Debug
f12::reload
```

```
^F12::

  clipboard =
  Send, ^c
  ClipWait, 1

  if ErrorLevel
  {
    MsgBox, The attempt to copy text onto the clipboard failed.
    Return
  }

  selection = %clipboard%
  Send, ^{t}
  Sleep 500
  SendInput http://www.spanishdict.com/translate/%selection%{Enter}
Return
```
