* http://secretsofinternet.ru/2009/02/26/namespaces-first-look/
* https://www.sitepoint.com/xml-namespaces-explained/

XPath
* Examples: https://docs.python.org/3/library/xml.etree.elementtree.html#elementtree-xpath
* Generator: http://xmltoolbox.appspot.com/xpath_generator.html

#### Python
:bulb: `xmltodict.parse` is much easier when no editing is needed

`xml.etree.ElementTree.register_namespace` works for serialization only. For "find*" methods use `namespaces` parameter.
```python
import xml.etree.ElementTree
xmlData = xml.etree.ElementTree.parse("autounattend.xml")
namespaces = {"unattend": "urn:schemas-microsoft-com:unattend"}
xmlData.find("./unattend:settings[@pass='windowsPE']/"
        "unattend:component[@name='Microsoft-Windows-International-Core-WinPE']", namespaces=namespaces).items()
xmlData.find("./unattend:settings[@pass='windowsPE']/"
        "unattend:component[@name='Microsoft-Windows-International-Core-WinPE']", namespaces=namespaces).getchildren()

# Unnamed namespaces
dvdImages = xmlData.find('{http://www.virtualbox.org/}Machine/{http://www.virtualbox.org/}MediaRegistry/{http://www.virtualbox.org/}DVDImages')
for image in dvdImages:
    dvdImages.remove(image)
```
