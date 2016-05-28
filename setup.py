import setuptools

def readme():
    with open("README.md") as f:
        return f.read()

setuptools.setup(name="ihnil",
                 version="1.0",
                 description="Python 'if' loop optimizer",
                 long_description=open("README.md").read(),
                 url="https://github.com/forstmeier/ihnil",
                 author="John Forstmeier",
                 author_email="john.forstmeier@gmail.com",
                 license="MIT",
                 packages=["ihnil"],
                 install_requires=["argparse", "os", "ast", "codegen"],
                 zip_safe=False)
