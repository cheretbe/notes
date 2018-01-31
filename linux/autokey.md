* https://github.com/autokey/autokey
* API docs: https://autokey.github.io/index.html

```python
system.create_file("/home/ubuntu/debug.txt", "my_var: %s" % my_var)


text = clipboard.get_selection()
keyboard.send_keys("<ctrl>+t")
time.sleep(0.2)
keyboard.send_keys("http://diccionario.ru/perevod/%s" % text)
keyboard.send_key("<enter>")


text = clipboard.get_selection()
keyboard.send_keys("<ctrl>+t")
time.sleep(0.2)
keyboard.send_keys("http://www.spanishdict.com/translate/%s" % text)
keyboard.send_key("<enter>")
```
