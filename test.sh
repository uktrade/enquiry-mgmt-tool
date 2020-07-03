#!/bin/bash -xe

docker-compose run app python -m pytest --cov -s --ds=app.settings.djangotest -vvv $@
