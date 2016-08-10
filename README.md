# Lifelog Eval

Evaluate lifelog annotations, and interact with them through an API.

## Setting up

### Requirements

YYMV, however, these are the tools and libraries I used in order to get
this system running.

 - elasticsearch `Version 2.2.0`
 - java `version "1.8.0_31"`
 - python `Python 3.5.1`

## Running the server

This project uses [gradle](https://gradle.org/) for building the server.

Before starting the server, ensure `elasticsearch` is running, _and_ 
these environment variables are set:

```
export LIFELOGEVAL_ELASTIC_URL="http://localhost/"
export LIFELOGEVAL_ELASTIC_INDEX="lifelog"
export LIFELOGEVAL_ELASTIC_CLUSTER="elasticsearch"
```

If you are on a unix system, you may execute `./gradlew installdist` 
which will build everything needed to run the server. After building, 
it can be started by running:

 - `build/install/lifelog-eval/bin/lifelog-eval server configuration.yml`

## Exporting data

After [importing the data](https://github.com/hscells/lifelog-sampling#importing-the-data),
and annotating some images somehow, it's time to export it for 
evaluation!

The `src/main/python/export-annotations.py` script will do this for you
and will export a JSON file that contains the annotations. For example:

```json
[
...
  {
    "image_id": "b00000782_21i6bq_20150218_151313e",
    "tags": [
      "computer screen",
      "keyboard",
      "office"
    ],
    "text": null,
    "query": "computer office",
    "assessments": {
      "headphones": 0,
      "juice": 0,
      "computer": 7,
      "car": 0,
      "office": 7
    }
  },
...
]
```

_Note_: for an annotation type with no annotation, the null value is
used. This is as per the JSON [specification](http://www.json.org/).