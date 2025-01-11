* https://regex101.com/

### Sublime text
Swap lines like that
```yaml
- "name": docker.domain.tld
  "login": docker
```
- <kbd>Ctrl</kbd>+<kbd>H</kbd>
- Find what: `^- ("login": [^\n]*)\n^..("name": [^\n]*)\n`
- Replace with: `- $2\n  $1\n` :bulb: $1 and $2 are references to [capturing groups](https://www.regular-expressions.info/brackets.html)
- check _Regular expression_
- **UNcheck** _case sensitive_
- check _Wrap_
- <kbd>Replace all</kdd>
- source: https://stackoverflow.com/questions/48455198/swap-line-text-in-sublime-text-3/48460185#48460185

### Python

Python's re is painfully slow for replacements in relatively large (~900k) buffers. Use Google's [RE2](https://github.com/google/re2/)

* https://github.com/google/re2/wiki/Syntax

```shell
pip3 install google-re2
```

```python
import re2

options = re2.Options()
# [!!] Looks like posix_syntax is not needed. Tried it to make \S work. But looks like with no
#      options at all it doesn't work. Passing as an options object without changing any properties
#      seems to fix it. ¯\_(ツ)_/¯
# # Without posix_syntax, perl_classes and one_line have no effect
# # https://github.com/google/re2/blob/6dcd83d60f7944926bfd308cc13979fc53dd69ca/re2/re2.h#L634
# options.posix_syntax = True
# # Enables (among others) \S
# options.perl_classes = True
# options.one_line = False

config, subs_num = re2.subn(pattern, replace, config, options=options)

for match in re2.finditer(pattern, config, options=options):
  pass
```
