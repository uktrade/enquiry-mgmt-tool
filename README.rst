Enquiry Management Tool
=======================

This is tool mainly used by the Service team to manage investment enquiries.
They can review enquiries, update them during their engagement with the
potential investors and submit the qualified ones to |data-hub|_.

Installation with Docker
------------------------

This project uses |docker-compose|_ to setup and run all the necessary components.
The |file-docker-compose|_ file provided is meant to be used for running tests and
development.

.. code-block:: bash

   $ git clone https://github.com/uktrade/enquiry-mgmt-tool.git
   $ cd enquiry-mgmt-tool

#.  Clone the repository:

#.  Bootstrap the project (install node dependencies and compile CSS from |scss|_)

    .. code-block:: bash

       $ sh ./bootstrap.sh

#.  Set up your ``app/settings/.env`` file:

    .. code-block:: bash

       $ cp sample_env app/settings/.env

#.  Build and run the necessary containers for the required environment:

    .. code-block:: bash

       $ docker-compose up --build

You can view the app at http://localhost:8000/enquiries/

The application uses SSO by default. When you access the above link for the
first time you will be redirected to SSO login page. After authentication it
will create a user in the database.

Configuration
-------------

The |file-sample_env|_ file contains all the required environment variable for the application.
Sample values are provided in this file but the actual values are to be included
in the ``app/settings/.env`` file at the appropriate location.

The actual values are added to ``ready-to-trade`` `vault`. Please use the values
corresponding to the ``dev`` environment.

Set up a flake8 pre-commit hook locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To set up a pre-commit hook which will prevent you from committing code with
formatting errors, run: ``make setup-flake8-hook``

Single Sign On (SSO)
^^^^^^^^^^^^^^^^^^^^

The app works out of the box with |mock-sso|_, which is part of the
|docker-compose|_ setup. The |oauth|_ flow however only works locally when you
set the ``AUTHBROKER_URL`` env var to ``host.docker.internal:8080``.
This is because the |mock-sso|_ service (configured with the ``AUTHBROKER_URL``)
must be accessible from outside of `docker-compose` for the `authorization redirect`,
and also from within `docker-compose` to make the `access token` POST request.
The problem though is that the service can only be accessed from another docker
container as ``http://mock-sso:8080``, which however is not available outside of
`docker-compose`. The special
`host.docker.internal <https://docs.docker.com/docker-for-mac/networking/#i-want-to-connect-from-a-container-to-a-service-on-the-host>`_
host name should be accessible from everywhere. Should it for any reason not
work, try ``docker.for.mac.localhost``. The value varies across platforms.

You can disable the SSO with the ``FEATURE_ENFORCE_STAFF_SSO_ENABLED`` env var:

.. code-block::

    FEATURE_ENFORCE_STAFF_SSO_ENABLED=1 # on
    FEATURE_ENFORCE_STAFF_SSO_ENABLED=0 # off

Or in ``app/settings/*``

.. code-block::

    ENFORCE_STAFF_SSO_ENABLED=True # on
    ENFORCE_STAFF_SSO_ENABLED=False # off

In which case, it will redirect to |django|_ admin page for login.

|oauth| Access Token Refreshment
""""""""""""""""""""""""""""""

|oauth|_ `access tokens` issued by |staff-sso|_ have expiration time of 10 hours so,
that it just about outlives a user's working time. In order to always have a valid
`access token` this app limits the user's session to 9 hours. When the session
expires, the user will be automatically redirected to ``/auth/login`` which will
refresh both the session and the `access token` and allows the user to use the
app uninterruptedly for another period of 9 hours.

The session expiration can be configured with the optional
``SESSION_COOKIE_AGE`` environmental variable which defaults to 9 hours.

Tests
-----

Unit tests
^^^^^^^^^^

The unit tests are written with |pytest|_. You can run all unit tests with:

.. code-block:: bash

   $ ./test.sh app

End to end tests
^^^^^^^^^^^^^^^^^^^^^^

The end to end tests (e2e) are written in JavaScript with |cypress|_.
You can run them in `watch` mode with:

.. code-block:: bash

   $ npm test

.. note::

   ``npm test`` expects the application to be listening on ``localhost:8000``

The `e2e` tests can also be run `headless` with:

.. code-block:: bash

   $ npx cypress run

or

.. code-block:: bash

   $ docker-compose run cypress

Allowing for Fixture Reset during e2e tests
"""""""""""""""""""""""""""""""""""""""""""

It is possible to expose a URL method which enables an external testing agent
(e.g. |cypress|_) to reset the database to a known fixture state.

Naturally this endpoint is not exposed by default. To enable it you must:

* Run Django with ``ROOT_URLCONF`` set to ``app.testfixtureapi_urls`` which includes the "reset" endpoint.
  This can be achieved by running Django with ``DJANGO_SETTINGS_MODULE`` set to either
  ``app.settings.djangotest`` (which is already set to be the case in pytest.ini) or
  ``app.settings.e2etest`` (which is already set to be the case in docker-compose.yml)
* Set the environment variable ``ALLOW_TEST_FIXTURE_SETUP`` to have the explicit
  exact value ``allow``.

Under these conditions (and only these conditions) when this endpoint receives a ``POST`` request
it will reset the application database to the state frozen in the files:

- |file-test_users.json|_
- |file-test_enquiries.json|_

Because this method removes all user data it will also invalidate any active
session which your test client holds.
For this reason the method also creates a standard user of your specification,
logs them in and returns the session info in the cookie headers of the response.
You must therefor supply this method with JSON which describes a new seed user like this:

.. code-block:: json

   {
     "username": "user123",
     "first_name": "Evelyn",
     "last_name": "User",
     "email": "evelyn@example.com"
   }

Documentation
-------------

Documentation is written in |rst|_ and |sphinx|_. The documentation source files
live in the |file-doc|_ directory.

* Always keep the documentation in sync with the code
* Try to provide a link to every external source of information, don't let
  future readers of the codebase waste their time by searching for things which
  could be just clicked through a link.
* Always specify all function arguments and return values with
  ``:param <name>:`` and ``:returns:`` |sphinx|_ directives. Idealy acompanied
  with ``:type <name>:`` and ``:rtype:`` to describe the expected types.
* When referencing other objects use the ``:func:``, ``:class:``, ``:mod:``, etc
  directives. You can use them to also reference objects from external libraries
  e.g. ``:class:`djang.http.HttpRequest```, provided they are properly
  linked through |intersphinx|_ (see the next point)
* When referencing objects from other libraries, always try to link them through
  |intersphinx|_ by adding a record to the ``intersphinx_mapping`` dictionary in
  `<doc/source/config.py>`_.

Compilation to HTML
^^^^^^^^^^^^^^^^^^^

.. note::

    Each of the documentation related commands require you to be in the
    |file-doc|_ directory.

To compile the docs to HTML you need to have installed both the project
dependencies listed in |file-requirements|_ and the `docs` dependencies listed
in |file-doc-requirements|_. The easiest way to install them is to run the
|file-doc-bootstrap|_ script:

.. code-block:: bash

   $ cd doc/
   # Create and activate virtual environment specific for docs compilation
   $ python3 -m venv .env
   & . .env/bin/activate
   # Install the merged dependencies
   $ sh doc/bootstrap.sh

You can then compile the HTML with:

.. code-block:: bash

   $ make html

The compiled HTML will then be in ``doc/build``.

.. rst_prolog (do not remove this comment, it is used in doc/source/config.py)

.. |data-hub| replace:: DataHub
.. _data-hub: https://readme.trade.gov.uk/docs/playbooks/datahub.html

.. |great| replace:: GREAT
.. _great: https://readme.trade.gov.uk/docs/playbooks/great.gov.uk-website.html

.. |data-hub-api| replace:: DataHub API
.. _data-hub-api: https://github.com/uktrade/data-hub-api#data-hub-api

.. |staff-sso| replace:: Staff SSO
.. _staff-sso: https://readme.trade.gov.uk/docs/howtos/staff-sso-integration.html

.. |mock-sso| replace:: Mock SSO
.. _mock-sso: https://github.com/uktrade/mock-sso

.. |cypress| replace:: Cypress
.. _cypress: https://www.cypress.io/

.. |oauth| replace:: OAuth 2.0
.. _oauth: https://oauth.net/2/

.. |activity-stream| replace:: Activity Stream
.. _activity-stream: https://readme.trade.gov.uk/docs/playbooks/activity-stream/index.html

.. |xlsx| replace:: XLSX
.. _xlsx: https://docs.microsoft.com/en-us/openspecs/office_standards/ms-xlsx/

.. |docker-compose| replace:: Docker Compose
.. _docker-compose: https://docs.docker.com/compose/

.. |scss| replace:: SCSS
.. _scss: https://sass-lang.com/documentation/syntax#scss

.. |pytest| replace:: pytest
.. _pytest: https://docs.pytest.org/

.. |django| replace:: Django
.. _django: https://www.djangoproject.com/

.. |rst| replace:: reStructuredText (RST)
.. _rst: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

.. |sphinx| replace:: Sphinx
.. _sphinx: https://www.sphinx-doc.org/

.. |intersphinx| replace:: sphinx.ext.intersphinx
.. _intersphinx: https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html

.. |file-docker-compose| replace:: ``docker-compose.yml``
.. _file-docker-compose: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/docker-compose.yml

.. |file-sample_env| replace:: ``sample_env``
.. _file-sample_env: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/sample_env

.. |file-doc| replace:: ``doc/``
.. _file-doc: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/doc

.. |file-test_enquiries.json| replace:: ``app/enquiries/fixtures/test_enquiries.json``
.. _file-test_enquiries.json: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/app/enquiries/fixtures/test_enquiries.json

.. |file-test_users.json| replace:: ``app/enquiries/fixtures/test_enquiries.json``
.. _file-test_users.json: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/app/enquiries/fixtures/test_users.json

.. |file-requirements| replace:: ``requirements.txt``
.. _file-requirements: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/app/requirements.txt

.. |file-doc-requirements| replace:: ``doc/requirements.txt``
.. _file-doc-requirements: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/app/doc/requirements.txt

.. |file-doc-bootstrap| replace:: ``doc/bootstrap.sh``
.. _file-doc-bootstrap: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/app/doc/bootstrap.sh
