* Help file (v5.5)
   * [Original CHM](./files/rar/WinRAR_5.50_help.chm)
   * [Converted HTML](./html_help/index.htm) (converted with https://www.aconvert.com/ebook/chm-to-html/)
```shell
# -ep1 - exclude base folder from names
# -ma[4|5] - specify a version of archiving format
# -m<n> - set compression method (0-5, 0 - store, 3 - default, 5 -best)
# -ap<path> - set path inside archive
rar a -ep1 -ma5 -m5 -apsubdir-name ~/path/to/archive.rar ~/path/to/directory/
```
