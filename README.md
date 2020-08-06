# msr

A simple command-line tool for measuring web performance.

## Installation

```
pip install .
```

msr requires python 3.7. Either your system should use this version of python3, or else you should use [pyenv](https://github.com/pyenv/pyenv) to make that version available.


## Usage
```
❯ msr --help
Usage: msr [OPTIONS] COMMAND [ARGS]...

  A tool formeasuring URL response time.

Options:
  -p, --parallelism INTEGER  [default: 10]
  --help                     Show this message and exit.

Commands:
  list
  measure         Displays the size of each registered URL.
  race            Displays the average response time by domain.
  register        Registers the provided URL
  response-times  Displays the response time of each registered URL.
  version         Displays the version of the program.
  ```

  ## Development

[`pipenv`](https://pipenv.pypa.io/en/latest/) can be used to set up a development environment:

```
pipenv install -e .
```

Library dependencies are declared in [setup.py](./setup.py), so that `msr` is available as a library (and installable via `pip install`). See [this guide](https://pipenv.pypa.io/en/latest/advanced/#pipfile-vs-setup-py).