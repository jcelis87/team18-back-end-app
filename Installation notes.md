# Installation notes
---

For Mac Big Sur

```
pip install pipenv
pipenv shell
pipenv install
```
I had problem with the package psycopg2. This [stackoverlfow post](https://stackoverflow.com/questions/65059310/apple-m1-install-psycopg2-package-symbol-not-found-pqbackendpid) helped.

```
brew install postgresql
pip install psycopg2-binary --force-reinstall --no-cache-dir
```