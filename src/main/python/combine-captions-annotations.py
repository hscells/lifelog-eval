"""
Combines two json files together to form one big annotations file suitable for import into the
elasticsearch index.

Uses python3
"""

import argparse, json


def combine(captions_file, annotations_file):
    """
    Combine a captions file with an annotations file to produce some combined file
    :param captions_file: the name of the captions JSON file
    :param annotations_file: the name of the annotations JSON file
    :return: a dictionary containing the merged files
    """
    with open(captions_file, 'r') as f:
        captions = json.loads(f.read())

    with open(annotations_file, 'r') as f:
        annotations = json.loads(f.read())

    annotated = []
    for annotation in annotations:
        image_id = annotation['id']
        annotated.append(image_id)

    for annotation in annotations:
        text = annotation['annotations']['text']
        if text is None or len(text) == 0:
            annotation['annotations']['text'] = captions[annotation['id']]

    for image_id, caption in captions.items():
        if ' ' not in image_id:
            caption = caption.replace('\t', '')
            if image_id not in annotated:
                annotations.append({'id': image_id,
                                    'annotations': {'text': caption, 'tags': None,
                                                    'query': None, 'assessments': None}})

    return annotations


def write_combined(combined, output_file):
    """
    Write a combined set of captions and annotations to a file
    :param combined: the combined dictionary
    :param output_file: the name of the output file
    :return:
    """
    with open(output_file, 'w') as f:
        f.write(json.dumps(combined, sort_keys=False, indent=2, separators=(',', ': ')))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Combine a caption file with annotations')
    argparser.add_argument('captions', help='captions file to load')
    argparser.add_argument('annotations', help='annotations file to load')
    argparser.add_argument('output', help='name of the output JSON file')

    args = argparser.parse_args()

    write_combined(combine(args.captions, args.annotations), args.output)
