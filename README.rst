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
    infos = wrapper.get_user_info()
    # It should return informations about your profile
    print(infos)
    # {
    #   'id': 1,
    #   'login': 'user',
    #   'email': 'email',
    #   'logas': False,
    #   'groups': ['student'],
    #   'login_date': '2021-04-07 23:38:36',
    #   'firstconnexion': False
    # }


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

Testing
-------

This package is available on Pypi. Simply install it using:

.. code:: bash

    git clone https://github.com/tbobm/etnawrapper
    cd etnawrapper
    pip install -e .
    pip install -r requirements-dev.txt
    pytest

Documentation
------------

You can generate the module documentation using:

.. code:: console

    $ pip install -r requirements-doc.txt
    $ make html
    $ cd build/html && python -m http.server
    Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...

Contibuting
-----------

Contibutions are welcome. Simply fork the project and make a pull
request.

Contributors
-----------

- `matteyeux <https://github.com/matteyeux/>`_
