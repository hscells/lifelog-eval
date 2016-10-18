"""
Filter the judged annotations based on the qrels
"""
import argparse
import json
import sys


def process(qrels_file, annotations_file):

    annotations = json.loads(annotations_file.read())

    ids = set()
    new_annotations = []

    for row in qrels_file.readlines():
        _, _, image_path, _ = row.split(' ')
        image_id = image_path.split('/')[-1].replace('.jpg', '')
        ids.add(image_id)

    for annotation in annotations:
        if annotation['id'] in ids:
            new_annotations.append(annotation)

    return json.dumps(new_annotations)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-q', '--qrels', help='The qrels file to load',
                           type=argparse.FileType('r'), default=sys.stdin)
    argparser.add_argument('-a', '--annotations', help='The annotations file to load',
                           type=argparse.FileType('r'), default=sys.stdin)
    argparser.add_argument('-o', '--output', help='The new annotations file',
                           type=argparse.FileType('w'), default=sys.stdin)

    args = argparser.parse_args()

    data = process(args.qrels, args.annotations)
    args.output.write(data)
