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
* Cookie AutoDelete: https://chrome.google.com/webstore/detail/cookie-autodelete/fhcgjolkccmbidfldomjliifgaodjagh
* uBlock Origin: https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm
* New Tab Redirect: https://chrome.google.com/webstore/detail/new-tab-redirect/icpgjfneehieebagbmdbhnlpiopdcmna
* Hoxx VPN Proxy: https://chrome.google.com/webstore/detail/hoxx-vpn-proxy/nbcojefnccbanplpoffopkoepjmhgdgh
* Selection Search: https://chrome.google.com/webstore/detail/selection-search/gipnlpdeieaidmmeaichnddnmjmcakoe?hl=en
    * https://diccionario.ru/perevod/%s
    * http://www.spanishdict.com/translate/%s
* Context Menu Search: https://chrome.google.com/webstore/detail/context-menu-search/ocpcmghnefmdhljkoiapafejjohldoga/related
```
[["-1","Multitran","https://www.multitran.ru/c/m.exe?CL=1&s=TESTSEARCH&l1=1",true],["-1","Wikipedia [RU]","https://ru.wikipedia.org/wiki/TESTSEARCH",true],["-1","Wikipedia [EN]","https://en.wikipedia.org/wiki/TESTSEARCH",true],["-1","Wikipedia [ES]","https://es.wikipedia.org/wiki/TESTSEARCH",true],["-1","diccionario.ru","https://diccionario.ru/perevod/TESTSEARCH",true],["-1","spanishdict.com","http://www.spanishdict.com/translate/TESTSEARCH",true]]
```
* Quick Tabs: https://chrome.google.com/webstore/detail/quick-tabs/jnjfeinjfmenlddahdjdmgpbokiacbbb?hl=en
* Tab Modifier: https://chrome.google.com/webstore/detail/tab-modifier/hcbgadmbdkiilgpifjgcakjehmafcjai?hl=en
