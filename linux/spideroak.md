```batch
:: View device numbers
"C:\Program Files\SpiderOakONE\SpiderOakONE.exe" --user-info
```

### Permanent deletion

![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) **Quit SpiderOak ONE before deletion**

```batch
:: Device number is optional and defaults to the current device
"C:\Program Files\SpiderOakONE\SpiderOakONE.exe" --device=2 --purge="C:\Documents and Settings\My Documents\unwanted.docx"
```
You can only delete data on a different device if you are using the same operating system.
For example, while seated at a Mac you cannot delete files that had been uploaded from device running Windows

Purge deleted items

```batch
"C:\Program Files\SpiderOakONE\SpiderOakONE.exe" --verbose --purge-deleted-items=PURGE_DAYS
```

* https://support.spideroak.com/hc/en-us/articles/115001891343-Command-Line-Reference
* https://support.spideroak.com/hc/en-us/articles/115001932006--purge
