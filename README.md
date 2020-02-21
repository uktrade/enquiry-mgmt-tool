# Enquiry Management Tool

This is tool mainly used by IST users to manage investment enquiries. They can review enquiries, update them during their engagement with the potential investors and submit the information to Data Hub.

## Installation with Docker

This project uses Docker compose to setup and run all the necessary components. The docker-compose.yml file provided is meant to be used for running tests and development.

1.  Clone the repository:

    ```shell
    git clone https://github.com/uktrade/enquiry-mgmt-tool.git
    cd enquiry-mgmt-tool
    ```

1.  Build the frontend styles:
    ```shell
    docker run -it --rm --name frontend -v "$(pwd):/app" node:10 bash -c 'cd /app && npm rebuild node-sass && npm install && npm run sass'
    ```

    To build the styles and watch for changes use the `sass:watch` script instead (this process will stay open in your shell): 

    ```shell
    docker run -it --rm --name frontend -v "$(pwd):/app" node:10 bash -c 'cd /app && npm rebuild node-sass && npm install && npm run sass:watch'
    ```

1.  Build and run the necessary containers for the required environment:

    ```shell
    cp sample_env app/.env
    docker-compose up -d && docker-compose logs -f api
    ```

## Loading initial data
1. Obtain a copy of the `enquiries.json` initial data fixture from the team and place it in a folder called fixtures in the enquiries app folder (it could be anywhere really as long its available to the apps docker container)
2. After initialising the docker container in a separate terminal shell into the app container `docker exec -it enquiry-mgmt-tool_api_1 /bin/bash`
3. from with the container run this command to load the data: `python manage.py loaddata app/enquiries/fixtures/enquiries.json`