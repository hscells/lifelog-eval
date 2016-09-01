# this script will perform the experiments and evaulate them
# usage:
# ./run-experiment.sh /path/to/topics.xml /path/to/output/runs.txt /path/to/NTCIR/qrels.txt
# $1=topics.xml $2=trec_run.txt $3=qrels.txt

## perform the actual experiments
python3 ./src/main/python/run-experiments.py $1 $2

## evaluate using trec eval
trec_eval -q $3 $2

