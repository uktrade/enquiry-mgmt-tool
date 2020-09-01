#!/usr/bin/env bash
# Merge project requirements with documentation requirements,
# exclude the psycopg2 package which is replaced with psycopg2-binary in
# documentation requirements.
pip install -r <(cat requirements.txt ../requirements.txt | grep -v psycopg2==)