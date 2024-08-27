# rbc.ua

> This python scraping utility is for educational purpose only.


## Installation

1. Install [Docker](https://www.docker.com) and [Pyenv](https://github.com/pyenv/pyenv).

2. Create dev environment:
```shell
$ pyenv install --skip-existing `$(pyenv local)`
$ python -m venv .venv
$ .venv/bin/pip install -r requirements.txt
```


## Run in development mode

```shell
$ docker compose run --build scraper /bin/bash
app@scraper:~$ python rbcua.py "tmp/data.csv"
app@scraper:~$ exit
```

## Start scraping

```shell
$ docker compose up --build
```
