# This script will get the annotations from the database

## the resulting file will be called annotations.json
python3 ./src/main/python/export-annotations.py annotations.json

## the captions.json can be created during the caption process (in lifelog-caption)
python3 src/main/python/combine-captions-annotations.py captions.json annotations.json combined.json
