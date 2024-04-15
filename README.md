# lsdo_test

<!---
[![Python](https://img.shields.io/pypi/pyversions/lsdo_test)](https://img.shields.io/pypi/pyversions/lsdo_test)
[![Pypi](https://img.shields.io/pypi/v/lsdo_test)](https://pypi.org/project/lsdo_test/)
[![Coveralls Badge][13]][14]
[![PyPI version][10]][11]
[![PyPI Monthly Downloads][12]][11]
-->

[![GitHub Actions Test Badge](https://github.com/LSDOlab/lsdo_test/actions/workflows/actions.yml/badge.svg)](https://github.com/lsdo_test/lsdo_test/actions)
[![Forks](https://img.shields.io/github/forks/LSDOlab/lsdo_test.svg)](https://github.com/LSDOlab/lsdo_test/network)
[![Issues](https://img.shields.io/github/issues/LSDOlab/lsdo_test.svg)](https://github.com/LSDOlab/lsdo_test/issues)


lsdo_test is a Python testing framework that builds on pytest and adds (1) testing of run scripts (examples and tutorials) and (2) tags for tests. 
In this testing framework, three types of files are treated as tests:

1. *Test scripts*. These scripts must be named `test_*.py`. 
Actual tests must be implemented as functions within these scripts named `test_*` 
and preceded by a directive, `##test {script_tags}`.
2. *Tutorial scripts*. These scripts must be named `tu_*.ipynb` and can contain tags specified via `##test {script_tags}`.
3. *Example scripts*. These scripts must be named `ex_*.py` and can contain tags specified via `##test {script_tags}`.

Note: For tutorials and examples, the line with the directive should be at or near the top of the file, but this is not enforced

Tests are run from the command line via `lsdo_test {command_prompt_tags}`.
This will recursively search within the current directory for all tests, tutorials, and examples.
If there is a match between `command_prompt_tags` and `script_tags`, the corresponding tests will be run.
If `script_tags` 
Running `lsdo_test` with the argument `-l` or `--list`
lists the found tests, tutorials, and examples and whether they will be run.

These tags arguments are simply lists of strings.
Any match between any command prompt and any script tag will result in the test script being run.
`*` in a tag is a wildcard—any match means the test will be run.
No directive means there is one tag, which is an empty string.
In command prompt, the backslash escape character must be used, i.e., `\*` instead of `*`.

# Installation

## Installation instructions for users
For direct installation with all dependencies, run on the terminal or command line
```sh
pip install git+https://github.com/LSDOlab/lsdo_test.git
```

## Installation instructions for developers
First clone the repository and install using pip.
On the terminal or command line, run
```sh
git clone https://github.com/LSDOlab/lsdo_test.git
pip install -e ./lsdo_test.git
```

# Getting started
1. Add one or more test, tutorial, or example scripts, as explained above.
2. Make sure these scripts have directives, in the form of `##test {script_tags}`, as explained above.
3. Run `lsdo_test /*` in terminal.