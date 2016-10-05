# Lifelog Eval

Evaluate lifelog annotations, and interact with them through an API.

## Setting up

### Requirements

YMMV, however, these are the tools and libraries I used in order to get
this system running.

 - elasticsearch `Version 2.2.0`
 - java `version "1.8.0_31"`
 - python `Python 3.5.1`
 - [trec_eval](https://github.com/hscells/homebrew-ir)

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
 
Alternatively, there is a script named `start-services.sh` which will
build and start everything automatically, so long as everything is 
installed.
 

## Running Experiments

Once you have the server started, you will need to import the data. I 
have some scripts I use to automate this process, `get-annotations.sh`
and `import-annotations.sh`. You can read below to see the format 
annotations need to be in to import the annotations. 

There is a shell script that can be run to perform experiments on the
data set. You will need some topics (that were distributed by NTCIR) and
you will need the qrels (for use in trec_eval).

This script can be invoked by running `./run-experiment.sh`. This script
takes two arguments:

 - The path to the topics file
 - The path to the qrels file
 
If you would like to run experiments for yourself, you can obtain the
data by visiting the [ntcir-12 website](http://research.nii.ac.jp/ntcir/permission/ntcir-12/perm-en-Lifelog.html).

## Rest Server
 
### Interacting with the server

 - delete the index `DELETE  /api/elastic/index`
 - add one or more documents to the index `POST    /api/elastic/index`
 - get a document from the index: `GET     /api/elastic/get/{id}`
 - query the index `GET     /api/elastic/search/{field}/{query}`
 - TREC-style query `POST     /api/eval/query`

When adding documents to the index, the format should look identical to
the format used when [exporting](#exporting-data) data (if you are doing
that).

When issuing a trec-style experiment to the service, the request should
look like this:

```json
{
  "fields": [
    "tags",
    "text"
  ],
  "topics": [
    {
      "queryId": "001",
      "query": "The Red Taxi",
      "description": "Find the moment(s) when I boarded a Red taxi, only to get out again shortly afterwards."
    },
    {
      "queryId": "002",
      "query": "Photographing a Lake",
      "description": "Find the moment(s) when I was taking photos of a lake."
    }
  ]
}
```

Importing data into elasticsearch can done by running the 
`import-annotations.sh` script. This will automatically export data from
the database and import it into the elasticsearch index.

### Exporting data

After [importing the data](https://github.com/hscells/lifelog-sampling#importing-the-data),
and annotating some images somehow, it's time to export it for 
evaluation!

The `src/main/python/export-annotations.py` script will do this for you
and will export a JSON file that contains the annotations. This is the 
structure needed for adding annotations for the index. For example:

```json
[
  {
    "id": "b00000782_21i6bq_20150218_151313e",
    "annotations": {
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
    }
  },
]
```

_Note_: for an annotation type with no annotation, the null value is
used. This is as per the JSON [specification](http://www.json.org/).