django-safety
=============

**Django application to list and disable user active sessions.**

This application is a lightweight version of `django-user-session`_.

The changes are:

* No middeware
* Does not touch to ``django.contrib.sessions``
* Does not touch to `django.contrib.sessions.middleware.SessionMiddleware`
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

.. _django-user-sessions: https://github.com/Bouke/django-user-sessions
