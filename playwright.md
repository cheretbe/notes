* https://playwright.dev/python/docs/api/class-playwright

```shell
# Debugging
# use .all() with .locator() .get_by_text() etc. or page object becomes unresponsive
# Most likely it waits for at least item to become available
page.screenshot(path="/test.png")
docker cp container_name:/test.png ~/temp/
```
Installation
```shell
# no Python
docker run -it --rm mcr.microsoft.com/playwright:v1.49.1-noble

# or (no Alpine: https://playwright.dev/docs/intro#system-requirements)
docker run --rm -it python:3.10-bullseye /bin/bash
pip install playwright

playwright install --with-deps chromium
# All browsers
playwright install-deps
playwright install
```


```python
import playwright.sync_api

# Interactive mode: https://playwright.dev/python/docs/library#interactive-mode-repl
# Use p.stop() when done
p = playwright.sync_api.sync_playwright().start()
browser = p.chromium.launch()
page = browser.new_page()
page.goto("https://62yun.ru/")

page.locator('.header__container_user_button-group_button').click()
page.locator('.modal-auth-email').fill('user@domain.tld')
page.locator('.modal-auth-password').fill("password")

page.get_by_role("button", name="Войти по email").click()
# https://playwright.dev/python/docs/api/class-frame#frame-wait-for-url
playwright.sync_api.expect(page.get_by_text("Мои серверы")).to_be_visible()

page.get_by_text("Мои серверы").click()
playwright.sync_api.expect(page.locator('.myservers__servers-group')).to_be_visible()

page.locator('.myservers__servers-group').inner_text()
page.locator('.myservers__servers-group').inner_html()
```
