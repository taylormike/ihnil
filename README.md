# IHNIL - I Hate Nested If Loops

## Description

Source-to-source AST transformation and optimization.  
Prounced: "eye-nil"  
For use on Python code modules. :snake:  
I hate nested "if" loops. They're ugly, they're slow, they've got to go.  
While there are *some* instances where they are necessary, let's see if we  
can get rid of all of the useless ones.  
This is an attempt to balance between **readability** and **optimization** all  
within Pythonic principles of code.  

## Usage

After installation, run via with the arguments below in the terminal:  

```
python3 reader.py [ -r/--read | -w/--read ] [ -h/--help ] filename  
```  

The default optional argument is ` -r / --read `.  
Currently only available for Python 3.  

## Dependencies

- [argparse](https://docs.python.org/3.4/library/argparse.html#module-argparse)
- [os](https://docs.python.org/3.4/library/os.html#module-os)
- [ast](https://docs.python.org/3.4/library/ast.html)
- [codegen](https://github.com/andreif/codegen)

## Contribution

Please adhere to ` pep8 ` standards when contributing to this project.  
- The official reference **style guide** can be found [here](https://www.python.org/dev/peps/pep-0008/)  
- The **command line tool** for static analysis of Python files can be found [here](https://pypi.python.org/pypi/pep8)  

Pull requests will only be accepted through [Github](https://github.com/)  

## Credits

**John Forstmeier**, *primary author*, [@forstmeier](https://github.com/forstmeier)  

**Mike Taylor**, *spiritual advisor*, [@taylormike](https://github.com/taylormike)  

Copyright (c) 2015-2016 John Forstmeier  
Released under the [MIT License](https://github.com/forstmeier/pythonistics/blob/master/LICENSE.txt)  

Logos designed on [logomakr.com](http://logomakr.com/)  
