# Enquiry Management Tool

This is tool mainly used by Service team to manage investment enquiries. They can review enquiries, update them during their engagement with the potential investors and submit the qualified ones to Data Hub.

## Installation with Docker

This project uses Docker compose to setup and run all the necessary components. The docker-compose.yml file provided is meant to be used for running tests and development.

1.  Clone the repository:

    ```shell
    git clone https://github.com/uktrade/enquiry-mgmt-tool.git
    cd enquiry-mgmt-tool
    ```

1.  Set up your .env file:
    ```shell
    cp sample_env app/settings/.env
    ```

1.  Build and run the necessary containers for the required environment:

    ```shell
    docker-compose up -d && docker-compose logs -f api
    ```

1.  Build the frontend styles:
    ```shell
    docker run -it --rm --name frontend -v "$(pwd):/app" node:10 bash -c 'cd /app && npm rebuild node-sass && npm install && npm run sass'
    ```

You can view the app at `http://localhost:8000/enquiries/`

The application uses SSO by default. When you access the above link for the first time you will be redirected to SSO login page. After authentication it will create a user in the database.

## Configuration

### sample_env
This file contains all the required environment variable for the application. Sample values are provided in this file but the actual values are to be included in the `.env` file at the appropriate location.

The actual values are added to `ready-to-trade` vault. Please use the values corresponding to the `dev` environment.

### SSO
Use the following ENV variable to toggle SSO:

    FEATURE_ENFORCE_STAFF_SSO_ENABLED=1 on
    FEATURE_ENFORCE_STAFF_SSO_ENABLED=0 off

Or in app/settings/*

    ENFORCE_STAFF_SSO_ENABLED=True on
    ENFORCE_STAFF_SSO_ENABLED=False off

It is possible to run the app with SSO disabled but it will redirect to Django admin page for login so a superuser needs to be created first.


## More useful info

If you already have the app container running and want to restart, you can use this:

```shell
docker-compose down -v -t0 && docker-compose up -d && docker-compose logs -f api
```


To build the styles and watch for changes use the `sass:watch` script instead (this process will stay open in your shell): 

    ```shell
    docker run -it --rm --name frontend -v "$(pwd):/app" node:10 bash -c 'cd /app && npm rebuild node-sass && npm install && npm run sass:watch'
    ```

For testing, you might want to load sample enquiries into the database. Sample data is available in json format, please ask the development team for more information.

### Running tests

To run all unit tests:

```
docker-compose run app python -m pytest -s -vvv app/enquiries/tests
```

To run an individual unit test, execute the following command:

```
pytest -s -vvv -k test_name app/enquiries
```

To run e2e tests:

```
docker-compose run cypress run --browser firefox
```

### Switching branches

Remember to rebuild images (where dependancies have changed) and deleting __pycache__ directories

Run the following from the project root to delete __pycache__ directories:

`find . -type d -iname __pycache__ -exec rm -Rf {} \;`
