"""
Filter the judged annotations based on the qrels
"""
import argparse
import json
import sys


def process(qrels_file, annotations_file):

    annotations = json.loads(annotations_file.read())

    qrels = {}
    new_annotations = {}

    for row in qrels_file.readlines():
        topic_id, _, image_path, _ = row.split(' ')
        image_id = image_path.split('/')[-1].replace('.jpg', '')
        if topic_id not in qrels.keys():
            qrels[topic_id] = set()
        else:
            qrels[topic_id].add(image_id)

    for topic_id in qrels.keys():
        for annotation in annotations:
            if annotation['id'] in qrels[topic_id]:
                if topic_id not in new_annotations.keys():
                    new_annotations[topic_id] = []
                else:
                    new_annotations[topic_id].append(annotation)

    return new_annotations


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-q', '--qrels', help='The qrels file to load',
                           type=argparse.FileType('r'), default=sys.stdin)
    argparser.add_argument('-a', '--annotations', help='The annotations file to load',
                           type=argparse.FileType('r'), default=sys.stdin)
    argparser.add_argument('-d', '--dest', help='The folder to output annotations to')

    args = argparser.parse_args()

    annotations = process(args.qrels, args.annotations)
    for topic_id, annotations in annotations.items():
        with open(args.dest + topic_id + '.json', 'w') as f:
            f.write(json.dumps(annotations, sort_keys=False, indent=2, separators=(',', ': ')))
