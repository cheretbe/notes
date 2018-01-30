* https://github.com/autokey/autokey
* API docs: https://autokey.github.io/index.html

```python
text = clipboard.get_selection()
#system.create_file("/home/ubuntu/debug.txt", "selection: %s" % text)
keyboard.send_keys("<ctrl>+t")
time.sleep(0.2)
keyboard.send_keys("http://www.spanishdict.com/translate/%s" % text)
keyboard.send_key("<enter>")
```
