# IHNIL - I Hate Nested If Loops

[![Join the chat at https://gitter.im/forstmeier/ihnil](https://badges.gitter.im/forstmeier/ihnil.svg)](https://gitter.im/forstmeier/ihnil?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://travis-ci.org/forstmeier/ihnil.svg?branch=master)](https://travis-ci.org/forstmeier/ihnil) [![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badge/)

## Description

Source-to-source AST transformation and optimization.  

Pronounced "EYE-nil"; for use on Python code modules. :snake:  

I hate nested "if" loops. They're ugly, they're slow, they've got to go.
While there are *some* instances where they are necessary, let's see if we
can get rid of all of the useless ones.  

This is an attempt to balance between **readability** and **optimization** all
within Pythonic principles of code.  

## Installation

The source code can be downloaded directly from GitHub.  

## Usage

After installation, run via the commands below in the terminal:  

`python3 reader.py [ -r/--read | -w/--write ] filename.py`  

The default argument is a simple printout of error line locations.
Currently only available for Python 3.  

## Contribution

Please adhere to ` pep8 ` standards when contributing to this project.  
- The official reference **style guide** can be found
[here](https://www.python.org/dev/peps/pep-0008/)  
- The **command line tool** for static analysis of Python files can be found
[here](https://pypi.python.org/pypi/pep8)  

Additionally, please include proper docstrings and follow the `pydocstyle`
guidelines for code.
- The **PEP 257** regarding docstrings can be found [here](https://www.python.org/dev/peps/pep-0257/)
- The **command line tool** to ensure proper style can be found [here](https://github.com/PyCQA/pydocstyle)  

Pull requests will only be accepted through [GitHub](https://github.com/)  

Keep all commit messages to approximately 60 characters, starting with an
imperative and ending without a period. Please follow a *merge-style*
workflow within your local repo.

Just a couple of syntactic preferences:
- Write all strings using double quotes -> `"string"`
- Create empty instances of objects using literals -> `list()`

## Credits

**John Forstmeier**, *primary author*,
[@forstmeier](https://github.com/forstmeier)  

**Mike Taylor**, *spiritual advisor*,
[@taylormike](https://github.com/taylormike)  

Copyright (c) 2015-2016 John Forstmeier  
Released under the [MIT License]
(https://github.com/forstmeier/pythonistics/blob/master/LICENSE.txt)  

Logos designed on [logomakr.com](http://logomakr.com/)  
