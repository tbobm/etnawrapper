from distutils.core import setup

__version__ = '1.1.1'

setup(
    name='etnawrapper',
    packages=['etnawrapper'],
    install_requires=[
        'requests',
    ],
    version=__version__,
    description='API wrapper for ETNA\' APIs',
    long_description=open('README.rst', 'r').read(),
    author='Theo Massard',
    author_email='massar_t@etna-alternance.net',
    url='https://github.com/massard-t/etnawrapper',
    download_url='https://github.com/massard-t/etnawrapper/archive/{}.tar.gz'.format(__version__),
    keywords=['school', 'wrapper', 'APIs'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
