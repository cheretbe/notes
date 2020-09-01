* `markdown-it` demo: https://markdown-it.github.io/
* Github Syntax highlighting list: https://github.com/github/linguist/blob/master/lib/linguist/languages.yml
* Gitlab references (issues, commits, etc): https://docs.gitlab.com/ce/user/markdown.html#special-gitlab-references
------
* http://ctan.altspu.ru/macros/latex/contrib/fancyhdr/fancyhdr.pdf
* https://tex.stackexchange.com/questions/139139/adding-headers-and-footers-using-pandoc
* https://tex.stackexchange.com/questions/91353/how-to-write-date-and-time-in-footer
* **https://github.com/Wandmalfarbe/pandoc-latex-template**
* example: ooo tim

```shell
# https://github.com/jgm/pandoc/releases/latest
# Markdown to docx
# gfm (GitHub-Flavored Markdown)
pandoc -f gfm -o vagrant.docx vagrant.md

# Markdown to PDF
apt install texlive-latex-recommended texlive-latex-extra
# Install texlive-xetex package for --pdf-engine=xelatex
pandoc -f gfm -o test.pdf test.md -V geometry:a4paper -V geometry:margin=2cm -V mainfont="Calibri" --pdf-engine=xelatex
```

Collapsible details content
<details>
  <summary>
    Show details
  </summary>

  * Your markdown content here
  * Note an empty line after the `</summary>` tag (markdown parsing in details fails without it)
</details>

```markdown
Collapsible details content
<details>
  <summary>
    Show details
  </summary>

  * Your markdown content here
  * Note an empty line after the `</summary>` tag (markdown parsing in details fails without it)
</details>
```

[Link](https://ya.ru) example
```markdown
[Link](https://ya.ru) example
```

:warning: Note with an exclamation
```markdown
:warning: Note with an exclamation
```
* List of GitHub markdown emoji: https://gist.github.com/rxaviers/7360908

| Code                          | Icon                   |
| ----------------------------- | ---------------------- |
| `:information_source:`        | :information_source:   |
| `:warning:`                   | :warning:              | 
| `:exclamation:`               | :exclamation:          |
| `:question:`                  | :question:             |
| `:grey_exclamation:`          | :grey_exclamation:     |
| `:grey_question:`             | :grey_question:        |
| `:point_right:`               | :point_right:          |
| `:bulb:`                      | :bulb:                 |
| `:pencil2:`                   | :pencil2:              |
| `:memo:`                      | :memo:                 |
| `:bangbang:`                  | :bangbang:             |
| `:heavy_check_mark:`          | :heavy_check_mark:     |
| `:x:`                         | :x:                    |
| `:white_check_mark:`          | :white_check_mark:     |


![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) (old) Note with an exclamation
```markdown
![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) (old) Note with an exclamation
```

:warning: review this TOC generator: https://github.com/thlorenz/doctoc
## Table of Contents
* [Item 1](#item-1)
* [Item with ' symbol](#item-with--symbol)
### Item 1
  Text
* [\[ TOC \]](#table-of-contents)
### Item with ' symbol
  Text
* [\[ TOC \]](#table-of-contents)
```markdown
## Table of Contents
* [Item 1](#item-1)
* [Item with ' symbol](#item-with--symbol)
### Item 1
  Text
* [\[ TOC \]](#table-of-contents)
### Item with ' symbol
  Text
* [\[ TOC \]](#table-of-contents)
```

| Col 1         | Col 2 (centered)    | Col 3 (right) |
| ------------- |:-------------------:| -------------:|
| line 1        | text                | text          |
| line 2        | text                | text          |
| line 3        | text                | text          |
```markdown
| Col 1         | Col 2 (centered)    | Col 3 (right) |
| ------------- |:-------------------:| -------------:|
| line 1        | text                | text          |
| line 2        | text                | text          |
| line 3        | text                | text          |
```
