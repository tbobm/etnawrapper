Etnawrapper
===========

Python wrapper made for my school's apis

Based on `a colleague's
documentation <https://github.com/josephbedminster/api-etna>`__

Usage
-----

.. code:: python

    from etnawrapper import EtnaWrapper

    wrapper = EtnaWrapper(login='your_login', password='your_passwd')

    # In order to check if you can access the APIs, try this:
    wrapper.get_infos()
    # It should return informations about your profile

Tools
------------
This package provides an executable called `etna`.
Using this program, you will be able to get informations without developping your own implementations.

Current features:

- List current activities

Below is an example usage of this program:

.. code:: bash

    $ etna activities
    # Acitivities per module

In order to enable autocompletion, please refer to `click's autocomplete documentation <https://click.palletsprojects.com/en/7.x/bashcomplete/>`_

For bash:

.. code:: bash
    eval "$(_ETNA_COMPLETE=source_bash etna )"


Installation
------------

This package is available on Pypi. Simply install it using:

.. code:: bash

    $ pip install etnawrapper

Contibuting
-----------

Contibutions are welcome. Simply fork the project and make a pull
request.

Contributors
-----------

- `matteyeux <https://github.com/matteyeux/>`_
