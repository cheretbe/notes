* https://extensionworkshop.com/documentation/enterprise/enterprise-distribution/#installation-using-windows-registry
    * :warning: If you install using the Windows Registry, Firefox will not automatically update your add-on. You will have to arrange to update the add-on using whatever installation process you choose external to Firefox
*  https://github.com/mozilla/policy-templates
      *  Policies can be specified using the Group Policy templates on Windows, Intune on Windows, configuration profiles on macOS, or by creating a file called policies.json
      * :point_right: `policies.json` variant as it's most simple and cross-platform: https://support.mozilla.org/en-US/kb/customizing-firefox-using-policiesjson
        * `%ProgramFiles%\Mozilla Firefox\distribution\policies.json` example:
        ```json
        {
          "policies": {
            "ExtensionSettings": {
              "uBlock0@raymondhill.net": {
                "installation_mode": "force_installed",
                "install_url": "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"
              }
            }
          }
        }
        ```
----------

* https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/
* https://addons.mozilla.org/en-US/firefox/addon/hoxx-vpn-proxy/
* https://addons.mozilla.org/en-US/firefox/addon/selection-context-search/

```json
{
  "sVersion": "5.18",
  "websiteList": [
    {
      "type": "recent",
      "recentLen": 1,
      "contexts": [
        "selection"
      ],
      "id": 1
    },
    {
      "type": "separator",
      "contexts": [
        "selection"
      ],
      "id": 2
    },
    {
      "type": "link",
      "name": "Diccionario",
      "address": "https://diccionario.ru/perevod?output_type=dicts&prefdict=join_es_ru&q=",
      "contexts": [
        "selection"
      ],
      "id": 38,
      "popup": true
    },
    {
      "type": "link",
      "name": "Spanishdict",
      "address": "http://www.spanishdict.com/translation/",
      "contexts": [
        "selection"
      ],
      "id": 37,
      "popup": true
    },
    {
      "type": "link",
      "name": "Forvo",
      "address": "https://forvo.com/search/?language_search_header=&word_search=",
      "contexts": [
        "selection"
      ],
      "id": 40,
      "popup": true
    },
    {
      "type": "link",
      "name": "Wiktionary En",
      "address": "https://en.wiktionary.org/wiki/Special:Search?search=",
      "contexts": [
        "selection"
      ],
      "id": 41,
      "popup": true
    },
    {
      "type": "link",
      "name": "Wikipedia",
      "address": "https://en.wikipedia.org/wiki/",
      "contexts": [
        "selection"
      ],
      "popup": true,
      "id": 7
    },
    {
      "type": "link",
      "name": "Open selected link",
      "address": "",
      "contexts": [
        "selection"
      ],
      "id": 25
    },
    {
      "type": "separator",
      "contexts": [
        "selection",
        "page",
        "frame",
        "tab"
      ],
      "id": 31
    },
    {
      "type": "bookmarks",
      "address": "Bookmarks Menu\\Search",
      "contexts": [
        "selection"
      ],
      "id": 32
    },
    {
      "type": "folder",
      "name": "Bookmarks",
      "folder": [
        {
          "type": "bookmarks",
          "address": "Bookmarks Menu\\Context Menu",
          "contexts": [
            "page",
            "frame",
            "tab"
          ],
          "id": 34
        }
      ],
      "id": 33
    },
    {
      "type": "separator",
      "contexts": [
        "selection"
      ],
      "id": 35
    },
    {
      "type": "options",
      "contexts": [
        "selection"
      ],
      "id": 36
    },
    {
      "type": "link",
      "name": "Startpage",
      "address": "https://www.startpage.com/do/search?hmb=1&cat=web&cmd=process_search&language=english&engine0=v1all&abp=1&t=air&nj=0&query=",
      "contexts": [
        "selection"
      ],
      "id": 39
    }
  ],
  "sMenuLabel": "Find '%s' using ...",
  "bShowPopup": true,
  "iPopupMaxColumns": 6,
  "iPopupIconSize": 21,
  "bClosePopupOnClick": true,
  "bClosePopupOnScroll": true,
  "bClosePopupOnTimeout": true,
  "iPopupCloseTimeout": 4,
  "bShowAddSearchPage": true,
  "bCopySelection": false,
  "sOpenSearchIn": "opnt",
  "oPlaceHolder": {
    "keywords": "~$S$~",
    "url": "~$U$~",
    "subdomain": "~$B$~",
    "domain": "~$D$~"
  }
}
```
