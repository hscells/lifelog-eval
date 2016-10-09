"""

"""

import argparse
import sys
import json


def transform(captions):
    captions = json.loads(captions.read())
    annotations = []
    for image_id, caption in captions.items():
        if ' ' not in image_id:
            caption = caption.replace('redblue', 'red blue')
            caption = caption.replace('bluered', 'red blue')
            caption = caption.replace('presentinglecturing', 'presenting lecturing')
            caption = caption.replace('lecturingpresenting', 'presenting lecturing')
            annotations.append({'id': image_id, 'annotations': {'text': caption,
                                                                'tags': None,
                                                                'assessments': None,
                                                                'query': None}})
    return json.dumps(annotations, sort_keys=False, indent=2, separators=(',', ': '))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--captions', help='captions JSON',
                           default=sys.stdin, type=argparse.FileType('r'), required=False)
    argparser.add_argument('-o', '--output', help='output file',
                           default=sys.stdout, type=argparse.FileType('w'), required=False)

    args = argparser.parse_args()
    args.output.write(transform(args.captions))
