# Enquiry Management Tool

This is tool mainly used by IST users to manage investment enquiries. They can review enquiries, update them during their engagement with the potential investors and submit the information to Data Hub.

## Installation with Docker

This project uses Docker compose to setup and run all the necessary components. The docker-compose.yml file provided is meant to be used for running tests and development.

1.  Clone the repository:

    ```shell
    git clone https://github.com/uktrade/enquiry-mgmt-tool.git
    cd enquiry-mgmt-tool
    ```

1.  Set up your .env file:
    ```shell
    cp sample_env app/.env
    ```

1.  Build and run the necessary containers for the required environment:

    ```shell
    docker-compose up -d && docker-compose logs -f api
    ```

1.  Build the frontend styles:
    ```shell
    docker run -it --rm --name frontend -v "$(pwd):/app" node:10 bash -c 'cd /app && npm rebuild node-sass && npm install && npm run sass'
    ```

1.  Load sample users data using fixtures:

    ```shell
    docker-compose run api bash
    python manage.py loaddata app/enquiries/fixtures/users.json
    ```

You can view the app at `http://localhost:8000/enquiries/`

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
