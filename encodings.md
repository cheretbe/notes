* https://en.wikipedia.org/wiki/Character_encoding
* https://p0w3rsh3ll.wordpress.com/2013/04/16/viewing-code-pages/
* https://devblogs.microsoft.com/powershell/outputencoding-to-the-rescue/
    * The reason we convert to ASCII when piping to existing executables is that most commands today do not process UNICODE correctly.  Some do, most don’t. 
    * Old version with some comments: https://blogs.msdn.microsoft.com/powershell/2006/12/11/outputencoding-to-the-rescue/
* https://stackoverflow.com/questions/22349139/utf-8-output-from-powershell
* https://habr.com/ru/post/321076/

[Good article](https://medium.com/@joffrey.bion/charset-encoding-encryption-same-thing-6242c3f9da0c) on charset and encoding difference. *Before the invention of Unicode, the code points defined by the charsets always directly matched their representation in bytes, thus there was no need to make a difference between charset and encoding. Therefore, ASCII, Latin1, Cp1252 etc. can be considered as character sets and encodings at the same time, hence the confusion.*

Powershell uses 3 code pages. 1 for the input and 2 for the output. Standard console input/output encoding are `[console]::InputEncoding` and `[console]::OutputEncoding`, but for the output being sent through the pipeline to native applications, there’s an automatic variable called `$OutputEncoding`.

There is (was?) [a bug](https://stackoverflow.com/questions/22349139/utf-8-output-from-powershell/22363632#22363632) with Powershell caching the output handle (Console.Out)
```powershell
# Seems to work ok on Win 8.1 with PS 4
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding.CodePage
[Console]::Out.Encoding.CodePage
```
