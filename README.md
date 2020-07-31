# Enquiry Management Tool

This is tool mainly used by Service team to manage investment enquiries. They can review enquiries, update them during their engagement with the potential investors and submit the qualified ones to Data Hub.

## Installation with Docker

This project uses Docker compose to setup and run all the necessary components. The docker-compose.yml file provided is meant to be used for running tests and development.

1.  Clone the repository:

    ```shell
    git clone https://github.com/uktrade/enquiry-mgmt-tool.git
    cd enquiry-mgmt-tool
    ```

2.  Bootstrap the project (install node dependencies and compile CSS from SASS)
    ```shell
    sh ./bootstrap.sh
    ```

3.  Set up your .env file:
    ```shell
    cp sample_env app/settings/.env
    ```

4.  Build and run the necessary containers for the required environment:

    ```shell
    docker-compose up --build
    ```

You can view the app at `http://localhost:8000/enquiries/`

The application uses SSO by default. When you access the above link for the first time you will be redirected to SSO login page. After authentication it will create a user in the database.

## Configuration

### sample_env
This file contains all the required environment variable for the application. Sample values are provided in this file but the actual values are to be included in the `.env` file at the appropriate location.

The actual values are added to `ready-to-trade` vault. Please use the values corresponding to the `dev` environment.

## Set up a flake8 pre-commit hook locally
To set up a pre-commit hook which will prevent you from committing code with formatting errors, run:
`make setup-flake8-hook`

### Single Sign On (SSO)

The app works out of the box with
[mock-sso](https://github.com/uktrade/mock-sso), which is part of the
docker-compose setup. The OAuth flow however only works locally when you
set the `AUTHBROKER_URL` to
[`host.docker.internal:8000`](http://docker.for.mac.localhost:8000/).
This is because the SSO service (configured with the `AUTHBROKER_URL`) must be
accessible from outside of docker-compose for the authorization redirect, and
also from within docker-compose to make the access token POST request.
The problem though is that the service can only be accessed from another docker
container as `http://mock-sso:8080`, which however is not available outside of
docker-compose. The special
[`host.docker.internal`](https://docs.docker.com/docker-for-mac/networking/#i-want-to-connect-from-a-container-to-a-service-on-the-host)
host name should be accessible from everywhere. Should it for any reason not
work, try `docker.for.mac.localhost`. The value varies across platforms.

You can disable the SSO with the `FEATURE_ENFORCE_STAFF_SSO_ENABLED` env var:

    FEATURE_ENFORCE_STAFF_SSO_ENABLED=1 on
    FEATURE_ENFORCE_STAFF_SSO_ENABLED=0 off

Or in app/settings/*

    ENFORCE_STAFF_SSO_ENABLED=True on
    ENFORCE_STAFF_SSO_ENABLED=False off

In which case, it will redirect to Django admin page for login so a superuser
needs to be created first.

### Running tests

To run all unit tests:

```
./test.sh app
```

To run e2e tests:

```shell
npm test
```

Or

```shell
docker-compose run cypress run --browser firefox
```

### Allowing for Fixture Reset during e2e tests

It is possible to expose a URL method which enables an external testing agent (e.g. Cypress) to
reset the database to a known fixture state.

Naturally this endpoint is not exposed by default. To enable it you must:

  - Run Django with `ROOT_URLCONF` set to `app.testfixtureapi_urls` which includes the "reset" endpoint.
    This can be achieved by running Django with `DJANGO_SETTINGS_MODULE` set to either
    `app.settings.djangotest` (which is already set to be the case in pytest.ini) or
    `app.settings.e2etest` (which is already set to be the case in docker-compose.yml)
  - Set the environment variable `ALLOW_TEST_FIXTURE_SETUP` to have the explicit
    exact value `allow`.

Under these conditions (and only these conditions) when this endpoint receives a `POST` request
it will reset the application database to the state frozen in the files:

  - [app/enquiries/fixtures/test_enquiries.json](app/enquiries/fixtures/test_enquiries.json)
  - [app/enquiries/fixtures/test_users.json](app/enquiries/fixtures/test_users.json)

Because this method removes all user data it will also invalidate any active session which your
test client holds.

For this reason the method also creates a standard user (`Owner` object) of your specification,
logs them in and returns the session info in the cookie headers of the response.

You must therefor supply this method with  JSON which describes a new seed user like this:
```json
{
    "username": "user123",
    "first_name": "Evelyn",
    "last_name": "User",
    "email": "evelyn@example.com"
}
```

The `Content-Type` for the call must therefore be `application/json`.

### Switching branches

Remember to rebuild images (where dependancies have changed) and deleting __pycache__ directories

Run the following from the project root to delete __pycache__ directories:

`find . -type d -iname __pycache__ -exec rm -Rf {} \;`
