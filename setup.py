import re
import setuptools


setuptools.setup(name="ihnil",
                 version="1.0.0",
                 description="Python 'if' loop optimizer",
                 url="https://github.com/forstmeier/ihnil",
                 license="MIT",
                 author="John Forstmeier",
                 packages=setuptools.find_packages(),
                #  install_requires=["argparse", "os", "ast", "codegen"],
                 entry_points={
                    "console_scripts": ["ihnil = ihnil.ihnil:main"]},)
