#!/usr/bin/env bash

cd $(dirname "$0")/..

docker compose run --rm pypacer watching_testrunner -- pytest --disable-warnings --tb=short $@
