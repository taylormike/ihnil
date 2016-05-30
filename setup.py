import re
import setuptools


version = re.search('^__version__\s*=\s*"(.*)"',
                    open("ihnil/ihnil.py").read(),
                    re.M).group(1)

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(name="ihnil",
                 version=version,
                 description="Python 'if' loop optimizer",
                 long_description=long_description,
                 url="https://github.com/forstmeier/ihnil",
                 license="MIT",
                 author="John Forstmeier",
                 author_email="john.forstmeier@gmail.com",
                 packages=setuptools.find_packages(),
                 install_requires=["argparse", "os", "ast", "codegen"],
                 entry_points={
                    "console_scripts": ["ihnil = ihnil.ihnil:main"]},)
