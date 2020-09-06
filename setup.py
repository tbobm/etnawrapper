from distutils.core import setup


__version__ = "2.9.0"
URL = "https://github.com/massard-t/etnawrapper/archive/{}.tar.gz".format(__version__)

setup(
    name="etnawrapper",
    packages=["etnawrapper"],
    # TODO: Use requiremnts.txt
    install_requires=['requests', 'click', 'arrow'],
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
    entry_points={"console_scripts": ["etna=etnawrapper.client:main"]},
)
