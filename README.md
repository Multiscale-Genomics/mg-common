# mg-common

[![Documentation Status](https://readthedocs.org/projects/mg-common/badge/?version=latest)](http://mg-common.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.org/Multiscale-Genomics/mg-common.svg?branch=master)](https://travis-ci.org/Multiscale-Genomics/mg-common) [![Code Health](https://landscape.io/github/Multiscale-Genomics/mg-common/master/landscape.svg?style=flat)](https://landscape.io/github/Multiscale-Genomics/mg-common/master)

Example pipelines file that is ready to run in the VRE matching the code in the HowTo documentation.

This repo structure workflows and tools can be forked and used as the base template for new tools and workflows. It should have all of the base functionality and is set up for unit testing and with pylint to ensure code clarity.

# Requirements
- pyenv and pyenv-virtualenv
- Python 2.7.12
- Python Modules:
  - pylint
  - pytest
  - mg-tool-api

Installation
------------

Directly from GitHub:

```
cd ${HOME}/code

git clone https://github.com/Multiscale-Genomics/mg-common.git

cd mg-common
```

Create the Python environment

```
pyenv-virtualenv 2.7.12 mg-common
pyenv activate mg-common
pip install -e .
pip install -r requirements.txt
```
