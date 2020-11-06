# Spring-Cloud-in-Python

![Pre-commit](https://github.com/my-sweet-home-2020/A-Cat/workflows/Pre-commit/badge.svg)

## Before starting to commit
TBD: `poetry` or `pipenv` or other package manager
CMT: Here I use `poetry` as an example first

Dev Python Version: 3.7.9

1. Download `poetry` by using:
``` bash
# For linux and unix-like users
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
# For windows user, you will need your powershell or just use the subsystem
# If you wish to use powershell, the follow cmd is for you
# (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```
2. Install existing dependencies
``` bash
# Running locally for dev / test env etc
poetry install
# On pp / prod
poetry install --no-dev
```

3. Add new package: never ever pip install :)
``` bash
# Example
poetry add django
# For dev only
poetry add --dev ipython
# If you wish to test something on you local but not add it to the "lock"
poetry add --no-root xxx
```

4. To run python or some other packages that offer cli
```bash
# Boot django server in local
poetry run python manage.py runserver
# Or a lazy way, just enable the shell
poetry shell
python manage.py runserver
```

5. After running `poetry install` on local, for the very first time. Please run:
``` bash
poetry run pre-commit install
```

6. Start to commit :)

## Test

1. Show test coverage report on terminal

`poetry run pytest --cov-report term --cov ${package} tests/`
