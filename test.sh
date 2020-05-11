#!/bin/bash -xe

docker-compose run app python -m pytest -s --ds=app.settings.djangotest -vvv $@
