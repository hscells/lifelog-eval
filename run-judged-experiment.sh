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

QRELS=./processed_lsat_qrels.txt
TABLES=./experiments/tables.latex
EXPERIMENTS=./experiments/judged-experiment

mkdir experiments &> /dev/null

#echo "processing qrels"
#python3 ./src/main/python/process-qrels.py $2 > ${QRELS}
#
echo "getting judged captions"
python3 src/main/python/judged-captions.py -q ${QRELS} -a $3 -d judged/

echo '' > ${EXPERIMENTS}.txt

for f in $(find ./judged/*json)
do
    echo "running experiment for ${f:9:3}"
    ./import-annotations.sh ${f}
    ## perform the actual experiments
    python3 ./src/main/python/experiments.py $1 -t ${f:9:3} -n ${f:9:3} -f text >> ${EXPERIMENTS}.txt
done
## evaluate using trec eval
trec_eval -q ${QRELS} ${EXPERIMENTS}.txt > ${EXPERIMENTS}.eval.txt


### create the tables file if it doesn't exist and clear it if it does
#echo '' > ${TABLES}
#
### generate tables for each of the results
#echo '% all' >> ${TABLES}
#python3 ./src/main/python/generate-latex.py --trec ${ALL}.eval.txt >> ${TABLES}
#echo '% text' >> ${TABLES}
#python3 ./src/main/python/generate-latex.py --trec ${TEXT}.eval.txt >> ${TABLES}
#echo '% tags' >> ${TABLES}
#python3 ./src/main/python/generate-latex.py --trec ${TAGS}.eval.txt >> ${TABLES}
#echo '% query' >> ${TABLES}
#python3 ./src/main/python/generate-latex.py --trec ${QUERY}.eval.txt >> ${TABLES}
#echo '% assessment' >> ${TABLES}
#python3 ./src/main/python/generate-latex.py --trec ${ASSESSMENT}.eval.txt >> ${TABLES}
