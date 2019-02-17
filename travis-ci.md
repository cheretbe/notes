* https://blog.travis-ci.com/2017-09-12-build-stages-order-and-conditions
* https://docs.travis-ci.com/user/build-stages/matrix-expansion/
------
* Add "[ci skip]" to a commit message, and Travis will automatically skip that build

Two different ways to distinguish a tag from regular push

```yaml
language: python
dist: xenial
python:
  - "3.4"
  - "3.5"
  - "3.6"
  - "3.7"
script: python -V

matrix:
  fast_finish: true
  include:
    - python: "3.7"
      if: tag IS present
      env: ['TAG_IS_PRESENT'] 
      script: echo "Tag is present"
```
```yaml
language: python
dist: xenial
python:
  - "3.4"
  - "3.5"
  - "3.6"
  - "3.7"
script: python -V

jobs:
  fast_finish: true
  include:
    - stage: deploy
      if: tag IS present
      language: python
      python: "3.7"
      install: skip
      script:
        - echo "Stage ==> deploy"
```
