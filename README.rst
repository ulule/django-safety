django-safety
=============

*Django application to control user sessions.*

Description
-----------

This application is a lightweight version of
`django-user-session <https://github.com/Bouke/django-user-sessions>`_.

The main changes are:

* No middeware
* Does not touch to ``django.contrib.sessions``
* Does not touch to ``django.contrib.sessions.middleware.SessionMiddleware``
* Works with any session engine

How it works
------------

1. User logs in
2. We connect the logic to the ``user_logged_in`` signal
3. We create a new ``safety.models.Session`` instance
4. User can see the list of her sessions (with IP, last activity and device information)
5. User can delete a given session in the list
6. We delete both the related ``safety.models.Session`` instance and related session in store
7. User can delete all active sessions excepted the current one
8. We proceed the same way: deleting instances and related sessions from store
9. User logs out
10. We connect the logic to the ``user_logged_out`` signal
11. We delete the related ``safety.models.Session`` instance

Installation
------------

First, you need to install GeoIP.

On OS X with Homebrew:

.. code-block:: bash

    brew install geoip

Then, you need GeoIP databases.

For Django >= 1.9, download City and Country databases as binary (not CSV):

http://dev.maxmind.com/geoip/geoip2/geolite2/

For Django 1.8, download City and Country legacy databases as binary (not CSV):

http://dev.maxmind.com/geoip/legacy/geolite/

Create a directory wherever you want and uncompress these archives this
directory. Once done, set ``GEOIP_PATH`` setting pointing to this directory:

.. code-block:: python

    GEOIP_PATH = '/absolute/path/to/maxmind/db/directory'

Now, let's install django-safety:

.. code-block:: bash

    $ pip install django-safety

In your ``settings.py``, add ``safety`` to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        # Your other apps here
        'safety',
    )

Synchronize the database:

.. code-block:: bash

    $ python manage.py migrate safety

Done.

Development
-----------

.. code-block:: bash

    # Install pip and virtualenv
    $ sudo easy_install pip
    $ sudo pip install virtualenv

    # Clone repository
    $ git clone https://github.com/ulule/django-safety.git

    # Setup your development environment
    $ cd django-safety
    $ make devenv
    $ source .venv/bin/activate

    # Download GeoIP databases
    $ make geoip
    
    # Launch test suite
    $ make test

    # Run the example project (default user username is "johndoe")
    $ make example-migrate
    $ make example-user
    $ make example-serve

Compatibility
-------------

- python 2.7: Django 1.8, 1.9
- Python 3.4: Django 1.8, 1.9
- Python 3.5: Django 1.8, 1.9
