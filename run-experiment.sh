#!/usr/bin/env bash
#
# Harry Scells 2016
#
# this script will perform the experiments and evaulate them
# usage:
# ./run-experiment.sh /path/to/topics.xml /path/to/NTCIR/qrels.txt

## check if rest server is running
nc -zc localhost 8080 &> /dev/null
if [ $? -ne 0 ]
then
    echo REST Server is not running
    exit 1
fi

## check if elasticsearch is running
nc -zc localhost 9200 &> /dev/null
if [ $? -ne 0 ]
then
    echo Elasticsearch is not running
    exit 1
fi

## define some vars
ALL=./experiments/all
TEXT=./experiments/text
TAGS=./experiments/tags
QUERY=./experiments/query
ASSESSMENT=./experiments/assessment
TABLES=./experiments/tables.latex
QRELS=./processed_lsat_qrels.txt

## create experiments folder if it doesn't exist
mkdir experiments &> /dev/null

## perform the actual experiments
python3 ./src/main/python/experiments.py $1 -n all -o ${ALL}.txt -f text -f tags -f query -f assessment
python3 ./src/main/python/experiments.py $1 -n text -o ${TEXT}.txt -f text
python3 ./src/main/python/experiments.py $1 -n tags -o ${TAGS}.txt -f tags
python3 ./src/main/python/experiments.py $1 -n query -o ${QUERY}.txt -f query
python3 ./src/main/python/experiments.py $1 -n assessment -o ${ASSESSMENT}.txt -f assessment

## create a processed qrels file that aligns with the ids in the experiments
python3 ./src/main/python/process-qrels.py $2 > ${QRELS}

## evaluate using trec eval
trec_eval -q ${QRELS} ${ALL}.txt > ${ALL}.eval.txt
trec_eval -q ${QRELS} ${TEXT}.txt > ${TEXT}.eval.txt
trec_eval -q ${QRELS} ${TAGS}.txt > ${TAGS}.eval.txt
trec_eval -q ${QRELS} ${QUERY}.txt > ${QUERY}.eval.txt
trec_eval -q ${QRELS} ${ASSESSMENT}.txt > ${ASSESSMENT}.eval.txt

## create the tables file if it doesn't exist and clear it if it does
echo '' > ${TABLES}

## generate tables for each of the results
echo '% all' >> ${TABLES}
python3 ./src/main/python/generate-latex.py --trec ${ALL}.eval.txt >> ${TABLES}
echo '% text' >> ${TABLES}
python3 ./src/main/python/generate-latex.py --trec ${TEXT}.eval.txt >> ${TABLES}
echo '% tags' >> ${TABLES}
python3 ./src/main/python/generate-latex.py --trec ${TAGS}.eval.txt >> ${TABLES}
echo '% query' >> ${TABLES}
python3 ./src/main/python/generate-latex.py --trec ${QUERY}.eval.txt >> ${TABLES}
echo '% assessment' >> ${TABLES}
python3 ./src/main/python/generate-latex.py --trec ${ASSESSMENT}.eval.txt >> ${TABLES}
