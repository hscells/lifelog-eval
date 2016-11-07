"""
Combines two json files together to form one big annotations file suitable for import into the
elasticsearch index.

Uses python3
"""

import argparse, json


def combine(file_one, file_two):
    """
    Combine a captions file with an annotations file to produce some combined file
    :param file_one: the name of the captions JSON file
    :param file_two: the name of the annotations JSON file
    :return: a dictionary containing the merged files
    """
    with open(file_one, 'r') as f:
        a1 = json.loads(f.read())

    with open(file_two, 'r') as f:
        a2 = json.loads(f.read())

    a2_annotations = {}
    for annotation in a2:
        image_id, annotations = annotation['id'], annotation['annotations']
        a2_annotations[image_id] = annotations

    data = []
    for annotation in a1:
        print(image_id)
        image_id, annotations = annotation['id'], annotation['annotations']
        for annotation_type, annotation_value in annotations.items():
            if image_id in a2_annotations and annotation_type in a2_annotations[image_id]:
                if annotation_value is None and \
                                a2_annotations[image_id][annotation_type] is not None:
                    annotations[annotation_type] = a2_annotations[image_id][annotation_type]
        data.append({'id': image_id, 'annotations': annotations})

    return data


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
    argparser.add_argument('file_one', help='annotations file to load')
    argparser.add_argument('file_two', help='annotations file to load')
    argparser.add_argument('output', help='name of the output JSON file')

    args = argparser.parse_args()

    write_combined(combine(args.file_one, args.file_two), args.output)
