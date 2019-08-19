import os

from distutils.core import setup


__version__ = "2.2.1"
URL = "https://github.com/massard-t/etnawrapper/archive/{}.tar.gz".format(__version__)

BASE_DIR = os.path.dirname(__file__)


with open(os.path.join(BASE_DIR, "requirements.txt")) as f:
    requirements = f.readlines()


setup(
    name="etnawrapper",
    packages=["etnawrapper"],
    install_requires=requirements,
    version=__version__,
    description="API wrapper for ETNA' APIs",
    author="Theo 'Bob' Massard",
    author_email="massar_t@etna-alternance.net",
    url="https://github.com/tbobm/etnawrapper",
    download_url=URL,
    keywords=["school", "wrapper", "APIs"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
