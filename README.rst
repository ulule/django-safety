django-safety
=============

.. image:: https://secure.travis-ci.org/ulule/django-safety.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/ulule/django-safety


**Generic Django application for safer user accounts.**

Features
--------

Sessions
~~~~~~~~

* User can see all active sessions
* User can disable a given active session
* User can disable all active sessions

Force password change
~~~~~~~~~~~~~~~~~~~~~

* Administrators can require a password change for any user

Workflows
---------

Sessions
~~~~~~~~

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

Force password change
~~~~~~~~~~~~~~~~~~~~~

1. Administrator creates a ``PasswordChange`` instance and sets ``required`` to ``True``
2. When user logs in, it will be redirected to password change form
3. Until the user does not change its password, it is not authorized to go elsewhere
4. User changes its password
5. It is now authorized to go elsewhere

Installation
------------

Installing prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~

GeoIP library must be installed on your server.

On OS X with Homebrew:

.. code-block:: bash

    brew install geoip

You also need the GeoIP databases.

For Django >= 1.9, download City and Country databases as binary (not CSV):

http://dev.maxmind.com/geoip/geoip2/geolite2/

For Django 1.8, download City and Country legacy databases as binary (not CSV):

http://dev.maxmind.com/geoip/legacy/geolite/

Create a directory wherever you want and uncompress these archives this
directory. Once done, set ``GEOIP_PATH`` setting pointing to this directory:

.. code-block:: python

    GEOIP_PATH = '/absolute/path/to/maxmind/db/directory'

Installing django-safety
~~~~~~~~~~~~~~~~~~~~~~~~

Install

.. code-block:: bash

    $ pip install django-safety

In your ``settings.py``, add ``safety`` to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        # Your other apps here.
        'safety',
    )

In your ``urls.py``, include ``safety.urls`` under ``safety`` namespace.

.. code-block:: python

    urlpatterns = [
        # Your other URLs here.
        url(r'^security/', include('safety.urls', namespace='safety')),
    ]

Synchronize the database:

.. code-block:: bash

    $ python manage.py migrate safety

Great. The session feature is ready.

If you want to enable the "force password change" feature, read the next.

Enabling "force password change" feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable this feature, you have two choices:

* You want to protect only specific views? Use ``password_change_required()`` decorator
* You want to protect your whole application? Use ``PasswordChangeMiddleware`` middleware

The decorator works as any Django view decorator.

.. code-block:: python

    #
    # In your urls.py
    #

    from safety.decorators import password_change_required
    from .views import protect_me

    urlpatterns = [
        # Other URLs here.
        url(r'^protect-me/$', password_change_required(protect_me)),
    ]

    #
    # Or in your views.py (it's up to you)
    #
    from django.shortcuts import render
    from safety.decorators import password_change_required

    @password_change_required
    def protect_me(request):
        return render(request, 'protect_me.html')

The middleware works as any Django middleware.

Add ``safety.middleware.PasswordChangeMiddleware`` middleware in your ``settings.py``:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'safety.middleware.PasswordChangeMiddleware',
    ]

Done.

Settings
--------

+-------------------------------------------+---------------------------------------------------------------------+
| Setting                                   | Description                                                         |
+===========================================+=====================================================================+
| ``SAFETY_LOGIN_REQUIRED_MIXIN_CLASS``     | The Python path to your own "login required" mixin class.           |
|                                           | Defaults to ``safety.mixins.LoginRequiredMixin``.                   |
+-------------------------------------------+---------------------------------------------------------------------+
| ``SAFETY_IP_RESOLVER``                    | The Python path to your own IP resolver callable.                   |
|                                           | Defaults to ``safety.resolvers.remote_addr_ip``.                    |
+-------------------------------------------+---------------------------------------------------------------------+
| ``SAFETY_DEVICE_RESOLVER``                | The Python path to your own device resolver callable.               |
|                                           | Defaults to ``safety.resolvers.device``.                            |
+-------------------------------------------+---------------------------------------------------------------------+
| ``SAFETY_LOCATION_RESOLVER``              | The Python path to your own location resolver callable.             |
|                                           | Defaults to ``safety.resolvers.location``.                          |
+-------------------------------------------+---------------------------------------------------------------------+

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

    # Launch test suite with tox to check compatibility
    $ tox

    # Run the example project (default user username is "johndoe")
    $ make example-migrate
    $ make example-user
    $ make example-serve

Contribute
----------

1. Create an issue (**before** submitting pull requests)
2. Submit your bug or feature request
3. You want to fix or code it yourself? Great! Fork the project
4. Create a branch, always add tests and make sure they all pass with ``tox``
5. Submit a pull request

Compatibility
-------------

- python 2.7: Django 1.8, 1.9
- Python 3.4: Django 1.8, 1.9
- Python 3.5: Django 1.8, 1.9
