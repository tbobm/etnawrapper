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

Installation
------------

This package is available on Pypi. Simply install it using:

.. code:: bash

    $ pip install etnawrapper

Contibuting
-----------

Contibutions are welcome. Simply fork the project and make a pull
request.
