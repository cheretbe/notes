* https://en.wikipedia.org/wiki/Character_encoding
* https://p0w3rsh3ll.wordpress.com/2013/04/16/viewing-code-pages/
* https://devblogs.microsoft.com/powershell/outputencoding-to-the-rescue/
    * The reason we convert to ASCII when piping to existing executables is that most commands today do not process UNICODE correctly.  Some do, most don’t. 
    * Old version with some comments: https://blogs.msdn.microsoft.com/powershell/2006/12/11/outputencoding-to-the-rescue/
* https://stackoverflow.com/questions/22349139/utf-8-output-from-powershell
* https://habr.com/ru/post/321076/

[Good article](https://medium.com/@joffrey.bion/charset-encoding-encryption-same-thing-6242c3f9da0c) on charset and encoding difference. *Before the invention of Unicode, the code points defined by the charsets always directly matched their representation in bytes, thus there was no need to make a difference between charset and encoding. Therefore, ASCII, Latin1, Cp1252 etc. can be considered as character sets and encodings at the same time, hence the confusion.*

| Char | Charset                    | Code Page | Encoding       | Codepoint<br>(number) | Binary             |
|------|----------------------------|-----------|----------------|----------------------:|--------------------|
| Ы    | Unicode                    | 65001     | UTF-8          | `U+042B`              |`0xD0AB` (2 bytes)  |
| Ы    | Unicode                    | 1200      | UTF-16         | `U+042B`              |`0x042B` (2 bytes)  |
| Ы    | Cyrillic (DOS)             | 866       | Direct mapping | `0x9B`                |`0x9B` (1 byte)     |
| Ы    | Cyrillic (Windows)         | 1251      | Direct mapping | `0xDB`                |`0xDB` (1 byte)     |
| Ы    | Western European (Windows) | 1252      | :x: No mapping | No character in this charset               |
| €    | Unicode                    | 65001     | UTF-8          | `U+20AC`              |`0xE282AC` (3 bytes)|
| €    | Unicode                    | 1200      | UTF-16         | `U+20AC`              |`0x20AC` (2 bytes)  |
| €    | Cyrillic (DOS)             | 866       | :x: No mapping | No character in this charset               |
| €    | Cyrillic (Windows)         | 1251      | Direct mapping | `0x88`                |`0x88` (1 byte)     |
| €    | Western European (Windows) | 1252      | Direct mapping | `0x80`                |`0x80` (1 byte)     |

## BOM
* https://en.wikipedia.org/wiki/Byte_order_mark

| Encoding    | Hex           | Decimal     | Bytes as CP1252 chars |
|-------------|---------------|-------------|-----------------------|
| UTF-8       | `EF BB BF`    | 239 187 191 | `ï»¿`                 |
| UTF-16 (BE) | `FE FF`	      | 254 255     | `þÿ`                  |
| UTF-16 (LE) | `FF FE`       | 255 254     | `ÿþ`                  |
| UTF-32 (BE) | `00 00 FE FF` | 0 0 254 255 | `^@^@þÿ`              |
| UTF-32 (LE) | `FF FE 00 00` | 255 254 0 0 | `ÿþ^@^@ `             |
   * (`^@` is the null character)
### Powershell

Powershell uses 3 code pages. 1 for the input and 2 for the output. Standard console input/output encoding are `[console]::InputEncoding` and `[console]::OutputEncoding`, but for the output being sent through the pipeline to native applications, there’s an automatic variable called `$OutputEncoding`.

There is (was?) [a bug](https://stackoverflow.com/questions/22349139/utf-8-output-from-powershell/22363632#22363632) with Powershell caching the output handle (Console.Out)
```powershell
# Seems to work ok on Win 8.1 with PS 4
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding.CodePage
[Console]::Out.Encoding.CodePage
```
```powershell
[system.Text.Encoding]::UTF8.GetBytes("€")
[System.Text.Encoding]::GetEncoding(1251).GetString([byte]0x88)
[System.Text.Encoding]::UTF8.GetString(([byte]0xE2,0x82,0xAC))

[char]([int]0x20AC)


[System.Text.Encoding]::GetEncodings() | Format-Table -AutoSize

[System.Text.Encoding]::Default
[System.Text.Encoding]::ASCII
[System.Text.Encoding]::UTF8
# UTF-16 LE
[System.Text.Encoding]::Unicode
# UTF-32 LE
[System.Text.Encoding]::UTF32
# UTF-16 BE
[System.Text.Encoding]::BigEndianUnicode

$oemEncoding = [System.Text.Encoding]::GetEncoding($Host.CurrentCulture.TextInfo.OEMCodePage)
$ansiEncoding = [System.Text.Encoding]::GetEncoding($Host.CurrentCulture.TextInfo.ANSICodePage)
# Powershell expects the output of a console command to be OEM-encoded and translates it to ANSI.
# But winrm.cmd is a wrapper around c:\windows\system32\winrm.vbs that already outputs ANSI text
& "winrm" | ForEach-Object { $ansiEncoding.GetString($oemEncoding.GetBytes($_)) }
```

### Python
```python
"€".encode("cp1251")
b"\x88".decode("cp1251")

b"\xE2\x82\xAC".decode("utf8").encode("cp1252")
# Replace missing characters with "?"
b"\xE2\x82\xAC".decode("utf8").encode("cp866", errors="replace")
```
