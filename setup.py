from distutils.core import setup

__version__ = '1.0'

setup(
    name='etnawrapper',
    packages=['etnawrapper'],
    version=__version__,
    description='API wrapper for ETNA\' APIs',
    author='Theo Massard',
    author_email='massar_t@etna-alternance.net',
    url='https://github.com/massard-t/etnawrapper',
    download_url='https://github.com/massard-t/etnawrapper/archive/{}.tar.gz'.format(__version__),
    keywords=['school', 'wrapper', 'APIs'],
    classifiers=[],
)
