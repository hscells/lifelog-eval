#!/usr/bin/env bash
# This script will automatically import the annotations from the database to an elasticsearch index
## ensure `./start-services.sh` has been run before running this script!
## ensure you also have curl installed before running this script!

## we are importing a new set of annotations, so it's probably safe to just delete the index
curl -X DELETE localhost:9200/lifelog/

curl -X PUT -H "Content-Type: application/json" -d @stemmer.json localhost:9200/lifelog/

## now we can import the annotations
curl -X POST -H "Content-Type: application/json" -d @$1 localhost:8080/api/elastic/index &> /dev/null
