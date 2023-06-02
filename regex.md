* https://regex101.com/

Sublime text
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
