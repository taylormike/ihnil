import re
import setuptools


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open("ihnil/ihnil.py").read(),
    re.M).group(1)

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")

setuptools.setup(name="ihnil",
                 version=version,
                 author="John Forstmeier",
                 author_email="john.forstmeier@gmail.com",
                 description="Python 'if' loop optimizer",
                 long_description=long_description,
                 url="https://github.com/forstmeier/ihnil",
                 license="MIT",
                 packages=["ihnil"]
                 entry_points={
                    "console_scripts": ["ihnil = ihnil.ihnil:main"]})
