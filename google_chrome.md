Change user agent string:
* Developer Tools (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>I</kbd>)
* Hamburger menu (vertical dots) > More tools > Network conditions
* disable the option `Select automatically` and choose `Chrome - Windows` from drop-down menu

Show full URL in the address bar
* `chrome://flags/#omnibox-context-menu-show-full-urls`
* Set "Context menu show full URLs" to `Enabled`
* Reload (restart) Chrome
* Right click on the address bar and select "Always show full URLs" option in the context menu


1. Stop http:// -> to https:// redirection for a visited site:

chrome://net-internals/#hsts<br>
~~Go to `chrome://net-internals` and select "HSTS" from the drop down. Enter `domain.tld` under "Delete domain" and
press the **Delete** button. In newer versions select `Domain Security Policy`~~, delete option is under `Delete domain security policies`.

2. Clear dns cache: `chrome://net-internals/#dns`

Extensions
* Tab Activate: https://chrome.google.com/webstore/detail/tab-activate/jlmadbnpnnolpaljadgakjilggigioaj/related
* Cookie AutoDelete: https://chrome.google.com/webstore/detail/cookie-autodelete/fhcgjolkccmbidfldomjliifgaodjagh
* uBlock Origin: https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm
* New Tab Redirect: https://chrome.google.com/webstore/detail/new-tab-redirect/icpgjfneehieebagbmdbhnlpiopdcmna
* Hoxx VPN Proxy: https://chrome.google.com/webstore/detail/hoxx-vpn-proxy/nbcojefnccbanplpoffopkoepjmhgdgh
* Selection Search: https://chrome.google.com/webstore/detail/selection-search/gipnlpdeieaidmmeaichnddnmjmcakoe?hl=en
    * https://diccionario.ru/perevod/%s
    * http://www.spanishdict.com/translate/%s
```
eyJzZWFyY2hFbmdpbmVzIjpbeyJoaWRlX29uX2NsaWNrIjp0cnVlLCJuYW1lIjoiZGljY2lvbmFyaW8iLCJ1cmwiOiJodHRwczovL2RpY2Npb25hcmlvLnJ1L3BlcmV2b2QvJXMifSx7ImhpZGVfb25fY2xpY2siOnRydWUsIm5hbWUiOiJzcGFuaXNoZGljdCIsInVybCI6Imh0dHA6Ly93d3cuc3BhbmlzaGRpY3QuY29tL3RyYW5zbGF0ZS8lcyJ9LHsiaGlkZV9vbl9jbGljayI6dHJ1ZSwibmFtZSI6ImZvcnZvIiwidXJsIjoiaHR0cHM6Ly9mb3J2by5jb20vc2VhcmNoLz9sYW5ndWFnZV9zZWFyY2hfaGVhZGVyPSZ3b3JkX3NlYXJjaD0lcyJ9LHsiaGlkZV9vbl9jbGljayI6dHJ1ZSwibmFtZSI6Indpa3Rpb25hcnkgZW4iLCJ1cmwiOiJodHRwczovL2VuLndpa3Rpb25hcnkub3JnL3dpa2kvU3BlY2lhbDpTZWFyY2g/c2VhcmNoPSVzIn0seyJoaWRlX29uX2NsaWNrIjp0cnVlLCJuYW1lIjoid2lraXBlZGlhIGVuIiwidXJsIjoiaHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvJXMifV0sInN0eWxlU2hlZXQiOiIiLCJvcHRpb25zIjp7ImJ1dHRvbiI6MSwibmV3dGFiIjp0cnVlLCJhY3RpdmF0b3IiOiJhdXRvIiwicmVtb3ZlX2ljb25zIjoibm8iLCJzaG93X2luX2lucHV0cyI6dHJ1ZSwiYmFja2dyb3VuZF90YWIiOmZhbHNlLCJrX2FuZF9tX2NvbWJvIjpbMTcsMF0sImNvbnRleHRfbWVudSI6ImRpc2FibGVkIiwidG9vbGJhcl9wb3B1cCI6ImVuYWJsZWQiLCJ0b29sYmFyX3BvcHVwX3N0eWxlIjoiZGVmYXVsdCIsInRvb2xiYXJfcG9wdXBfaG90a2V5cyI6ZmFsc2UsInRvb2xiYXJfcG9wdXBfc3VnZ2VzdGlvbnMiOnRydWUsInNlcGFyYXRlX21lbnVzIjpmYWxzZSwiaGlkZV9vbl9jbGljayI6ZmFsc2UsImRpc2FibGVfZm9ybWV4dHJhY3RvciI6ZmFsc2UsIm9wZW5fb25fZGJsY2xpY2siOmZhbHNlLCJkYmxjbGlja19pbl9pbnB1dHMiOnRydWUsIm9wZW5fbmV3X3RhYl9sYXN0IjpmYWxzZSwiZGlzYWJsZV9lZmZlY3RzIjpmYWxzZSwiYXV0b19wb3B1cF9yZWxhdGl2ZV90b19tb3VzZSI6ZmFsc2UsImF1dG9fcG9wdXBfc2hvd19tZW51X2RpcmVjdGx5Ijp0cnVlLCJhdXRvX3BvcHVwX2luX2lucHV0cyI6ZmFsc2UsImFjdGl2YXRvcl9jb21ibyI6W10sInNob3dfdG9vbHRpcHMiOmZhbHNlLCJjaXJjdWxhcl9tZW51IjpmYWxzZSwic29ydF9ieV9jbGljayI6ZmFsc2UsInNlbGVjdGlvbl9sZW5ndGhfbGltaXQiOi0xLCJhdXRvX2hpZGVfZGVsYXkiOjAsImF1dG9fb3Blbl9kZWxheSI6MzAwLCJoaWRlX29uX3Njcm9sbCI6ZmFsc2UsInNlbGVjdGlvbl9hbGxvd19uZXdsaW5lIjpmYWxzZSwidXNlX3doaXRlbGlzdCI6ZmFsc2V9LCJWRVJTSU9OIjoiMC44LjU2In0=
```
* Context Menu Search: https://chrome.google.com/webstore/detail/context-menu-search/ocpcmghnefmdhljkoiapafejjohldoga/related
```
[["-1","diccionario.ru","https://diccionario.ru/perevod/TESTSEARCH",true],["-1","spanishdict.com","http://www.spanishdict.com/translate/TESTSEARCH",true],["-1","Multitran","https://www.multitran.ru/c/m.exe?CL=1&s=TESTSEARCH&l1=1",true],["-1","Wikipedia [RU]","https://ru.wikipedia.org/wiki/TESTSEARCH",true],["-1","Wikipedia [EN]","https://en.wikipedia.org/wiki/TESTSEARCH",true],["-1","Wikipedia [ES]","https://es.wikipedia.org/wiki/TESTSEARCH",true],["-1","forvo","https://forvo.com/search/TESTSEARCH/",true]]
```
* Quick Tabs: https://chrome.google.com/webstore/detail/quick-tabs/jnjfeinjfmenlddahdjdmgpbokiacbbb?hl=en
* Tab Modifier: https://chrome.google.com/webstore/detail/tab-modifier/hcbgadmbdkiilgpifjgcakjehmafcjai?hl=en
