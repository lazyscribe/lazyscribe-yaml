[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![PyPI](https://img.shields.io/pypi/v/lazyscribe-yaml)](https://pypi.org/project/lazyscribe-yaml/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lazyscribe-yaml)](https://pypi.org/project/lazyscrib-yaml/) [![codecov](https://codecov.io/gh/lazyscribe/lazyscribe-yaml/graph/badge.svg?token=W5TPK7GX7G)](https://codecov.io/gh/lazyscribe/lazyscribe-yaml)

# YAML-based artifact handling for lazyscribe

`lazyscribe-yaml` is a lightweight package that adds the following artifact handlers for `lazyscribe`:

* `yaml` — backed by [PyYAML](https://pyyaml.org/)
* `yaml12` — backed by [py-yaml12](https://github.com/posit-dev/py-yaml12), a YAML 1.2-compliant parser with fewer footguns and no transitive dependencies

# Installation

Python 3.10 or above is required. Use `pip` to install:

```console
$ python -m pip install lazyscribe-yaml
```

Both handlers are included by default; no extras are required.

# Usage

To use this library, simply log an artifact to a `lazyscribe` experiment or repository with `handler="yaml"` or `handler="yaml12"`.

## `yaml` handler (PyYAML)

```python
from lazyscribe import Project

project = Project("project.json", mode="w")
with project.log("My experiment") as exp:
    exp.log_artifact(name="feature-names", value=["a", "b", "c"], handler="yaml")

project.save()
```

## `yaml12` handler (py-yaml12)

The `yaml12` handler uses `py-yaml12`, which follows the YAML 1.2 specification. This avoids common PyYAML pitfalls such as unquoted booleans (`yes`/`no`/`on`/`off`) and octal literals being misinterpreted.

```python
from lazyscribe import Project

project = Project("project.json", mode="w")
with project.log("My experiment") as exp:
    exp.log_artifact(name="feature-names", value=["a", "b", "c"], handler="yaml12")

project.save()
```
