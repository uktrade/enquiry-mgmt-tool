=======================
Enquiry Management Tool
=======================

.. note::

    You can read the compiled documentation
    `here <https://uktrade.github.io/enquiry-mgmt-tool>`_.
    You should also read the |em-playbook|_ in the |dit-docs|_.

The *Enquiry Management Tool* is a web application designed for the
needs of the |ist|_ based in Belfast, to simplify the management of *investment
enquiries*. It allows for:

* Reviewing *enquiries*
* Updating them during their engagement with potential investors
* Submitting them to |data-hub|_
* The batch import and export of *enquiries* in the form of *CSV* file

The application also periodically ingests new *enquiries* from |activity-stream|_,
which were submitted through the |great|_ |investment-form|_.

Technical Overview
------------------

The *Enquiry Management* is a |drf|_ web application. It uses:

* |postgresql|_ database as the persistence layer
* |es|_ for *enquiry* search
* |scss|_ with |bem|_ methodology for CSS
* |gds-components|_ for the UI
* |celery|_ for periodic tasks and |activity-stream|_ ingestion
* |redis|_ as a backend for both the *session* and the |celery|_ *message queue*
* |docker-compose|_ for managing service dependencies in development and CI only
* |cypress|_ for *end to end (e2e)* tests
* |pytest|_ for unit tests
* |oauth|_ protocol for user authentication
* |hawk|_ protocol for inter-service communication authorization
* |flake8|_ as a *linter* for Python code
* |sphinx|_ for documentation

The application also depends on the |data-hub-api|_ and |activity-stream|_ services.

For information about deployment to the *dev*, *staging* and *production*
environments, refer to the
`Enquiry Management section <https://readme.trade.gov.uk/docs/playbooks/enquiry-management.html?highlight=enq>`_
in the `DDaT Readme <https://readme.trade.gov.uk/>`_.

Coding Style (linting)
^^^^^^^^^^^^^^^^^^^^^^

The style of Python code is enforced with |flake8|, which is run against new
code in a PR. You can set up a pre-commit hook to catch any formatting errors
in updated code by:

.. code-block:: bash

    $ make setup-flake8-hook

.. warning::

    This creates a new `./env` Python virtual environment.

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

    Note when running Apple Mac M1 silicon chipset and you get an error:
    .. code-block:: 
       runtime: failed to create new OS thread (have 2 already; errno=22) fatal error: newosproc
    In Dockerfile Use RUN wget for Apple instead of amd64.

    .. code-block:: bash

       $ docker-compose up --build

You can view the app at http://localhost:8001

The application uses SSO by default. When you access the above link for the
first time you will be redirected to SSO login page. After authentication it
will create a user in the database.

Configuration
-------------

The |file-sample_env|_ file contains all the required environment variable for the application.
Sample values are provided in this file but the actual values are to be included
in the ``app/settings/.env`` file at the appropriate location.

The actual values are added to the `Parameter store <https://eu-west-2.console.aws.amazon.com/systems-manager/parameters?region=eu-west-2&tab=Table#>`_.
Ensure you are in the correct AWS account when accessing the parameter store. For dev, uat and staging use the
``datahub`` account when accessing the `AWS account page <https://uktrade.awsapps.com/start/#/?tab=accounts>`_
Once in the parameter store, you can filter for the ``dev`` environment.

.. admonition:: Gov PaaS will be deprecated from July 2024 and keys will be moved from Vault to Parameter Store.
   :class: warning

   The actual values are added to ``ready-to-trade`` `vault`. Please use the values
   corresponding to the ``dev`` environment.

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

Consent Service
^^^^^^^^^^^^^^^^^^^^
To disable usage of Consent Service during development use ``FEATURE_ENFORCE_CONSENT_SERVICE`` env var. Set your local ``.env`` file like this:

.. code-block::

    FEATURE_ENFORCE_CONSENT_SERVICE=0

|oauth| Access Token Refreshment
""""""""""""""""""""""""""""""""

|oauth|_ `access tokens` issued by |staff-sso|_ have expiration time of 10 hours so,
that it just about outlives a user's working time. In order to always have a valid
`access token` this app limits the user's session to 9 hours. When the session
expires, the user will be automatically redirected to ``/auth/login`` which will
refresh both the session and the `access token` and allows the user to use the
app uninterruptedly for another period of 9 hours.

The session expiration can be configured with the optional
``SESSION_COOKIE_AGE`` environmental variable which defaults to 9 hours.

Visual Component Styles
-----------------------

The CSS stylesheets are written in |scss|_ in the |file-sass| directory.
All class names should conform to the |bem|_ methodology.

We rely on |gds-components|_ and its |govuk-frontend|_ |scss|_ package
to provide the main UI component markup and style. We should strive to use the
components with their default styling and only override the styles if there is a very
good reason for it. Most developers feel an urge to tweak the stiles slightly
to their subjective taste. **You should resist this urge at all times!**

Tests
-----

In accordance with our testing philosophy, the *end to end* tests are the
ones we rely on. The *unit tests* are optional and should be used mainly
as an aid during the development. Keep in mind, that unit tests only make sense
if they are written before the actual tested code.
Most of the unit tests in this project are legacy code.

.. _unit-tests:

Unit tests
^^^^^^^^^^

The unit tests are written with |pytest|_. You can run all unit tests with:

.. code-block:: bash

   $ ./test.sh app

.. _e2e-tests:

End to end tests
^^^^^^^^^^^^^^^^

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

   $ docker-compose run cypress run --browser chrome

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

Running locally with Data Hub API
---------------------------------

The Enquiry Management Tool application integrates with the `Data Hub API <https://github.com/uktrade/data-hub-api>`_.
The EMT fetches metadata from the Data Hub API and creates an investment project if an enquiry is successful.

* Run the Data Hub API following the `instructions in the repository's README <https://github.com/uktrade/data-hub-api#installation-with-docker>`_
* In your .env file in the data-hub-api repository, find the ``DJANGO_SUPERUSER_EMAIL`` variable
* From the top level of the data-hub-api repository, run the following command using the value of the variable above:

   ``docker exec data-hub_api_1 python manage.py add_access_token DJANGO_SUPERUSER_EMAIL``

* Copy the token from your terminal and add it as the value of the ``MOCK_SSO_TOKEN`` environment variable in the .env file of the enquiry-mgmt-tool repository
* Also in the enquiry-mgmt-tool .env file, set the value of the ``MOCK_SSO_EMAIL_USER_ID`` and ``MOCK_SSO_USERNAME`` environment variables to the same email address you created the token for
* Follow the instructions at the top of this file to run the Enquiry Management Tool application
* You can check that the integration with Data Hub is working correctly by going to http://localhost:8000/enquiries/1/edit and making sure that a list of names appears in the 'Client Relationship Manager' field dropdown


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

Hosting the compiled documentation
""""""""""""""""""""""""""""""""""

There is a |ci-workflow|_ defined in |file-ci-config|_ which compiles
and deploys the documentation to the |gh-pages|_ branch of the |repository|_
when code is pushed to the ``main`` branch, which is after every PR merge.
The deployed documentation will then be available at
`<https://uktrade.github.io/enquiry-mgmt-tool>`_.


.. rst_prolog (do not remove this comment, it is used in doc/source/config.py)

.. |repository| replace:: repository
.. _repository: https://github.com/uktrade/enquiry-mgmt-tool/

.. |gh-pages| replace:: ``gh-pages``
.. _gh-pages: https://github.com/uktrade/enquiry-mgmt-tool/tree/gh-pages

.. |data-hub| replace:: DataHub
.. _data-hub: https://readme.trade.gov.uk/docs/playbooks/datahub.html

.. |great| replace:: GREAT
.. _great: https://readme.trade.gov.uk/docs/playbooks/great.gov.uk-website.html

.. |dit-docs| replace:: DBT Software Development Manual
.. _dit-docs: https://readme.trade.gov.uk

.. |em-playbook| replace:: Enquiry Management playbook
.. _em-playbook: https://readme.trade.gov.uk/docs/playbooks/enquiry-management.html

.. |investment-form| replace:: Contact the investment team form
.. _investment-form: https://www.great.gov.uk/international/invest/contact/

.. |ist| replace:: Investment Services Team
.. _ist: https://www.gov.uk/government/organisations/uk-trade-investment/about-our-services#investment-services-for-non-uk-businesses

.. |data-hub-api| replace:: DataHub API
.. _data-hub-api: https://github.com/uktrade/data-hub-api#data-hub-api

.. |gds| replace:: GDS
.. _gds: https://design-system.service.gov.uk/

.. |gds-components| replace:: |gds|_ Components
.. _gds-components: https://design-system.service.gov.uk/components/

.. |govuk-frontend| replace:: GOV.UK Frontend
.. _govuk-frontend: https://frontend.design-system.service.gov.uk/

.. |staff-sso| replace:: Staff SSO
.. _staff-sso: https://readme.trade.gov.uk/docs/howtos/staff-sso-integration.html

.. |mock-sso| replace:: Mock SSO
.. _mock-sso: https://github.com/uktrade/mock-sso

.. |cypress| replace:: Cypress
.. _cypress: https://www.cypress.io/

.. |oauth| replace:: OAuth 2.0
.. _oauth: https://oauth.net/2/

.. |circle-ci| replace:: CircleCI
.. _circle-ci: https://app.circleci.com/pipelines/github/uktrade/enquiry-mgmt-tool

.. |ci-workflow| replace:: |circle-ci|_ workflow
.. _ci-workflow: https://circleci.com/docs/2.0/workflows-overview/

.. |activity-stream| replace:: Activity Stream
.. _activity-stream: https://readme.trade.gov.uk/docs/playbooks/activity-stream/index.html

.. |xlsx| replace:: XLSX
.. _xlsx: https://docs.microsoft.com/en-us/openspecs/office_standards/ms-xlsx/

.. |docker-compose| replace:: Docker Compose
.. _docker-compose: https://docs.docker.com/compose/

.. |scss| replace:: SCSS
.. _scss: https://sass-lang.com/documentation/syntax#scss

.. |bem| replace:: BEM
.. _bem: https://en.bem.info/methodology/

.. |es| replace:: Elastic Search
.. _es: https://www.elastic.co/

.. |postgresql| replace:: PostgreSQL
.. _postgresql: https://www.postgresql.org/

.. |redis| replace:: Redis
.. _redis: https://redis.io

.. |hawk| replace:: Hawk
.. _hawk: https://github.com/outmoded/hawk

.. |celery| replace:: Celery
.. _celery: http://celeryproject.org/

.. |pytest| replace:: pytest
.. _pytest: https://docs.pytest.org/

.. |django| replace:: Django
.. _django: https://www.djangoproject.com/

.. |drf| replace:: Django REST framework
.. _drf: https://www.django-rest-framework.org/

.. |flake8| replace:: Flake8
.. _flake8: https://flake8.pycqa.org/

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

.. |file-sass| replace:: ``sass/``
.. _file-sass: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/app/sass/

.. |file-ci-config| replace:: ``.circleci/config.yml``
.. _file-ci-config: https://github.com/uktrade/enquiry-mgmt-tool/blob/master/.circleci/config.yml