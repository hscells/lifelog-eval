# python3

import argparse, json, re, operator
import matplotlib.pyplot as plt

concepts_regex = re.compile(r'[^a-zA-Z0-9-]+')


def string_to_concepts(string):
    return concepts_regex.sub(' ', string).lower().strip().split(' ')


def analyse(input_file):

    concepts = {}

    with open(input_file) as f:
        annotations = json.loads(f.read())

    for annotation in annotations:
        image_annotations = annotation['annotations']
        tags = image_annotations['tags']
        text = image_annotations['text']
        query = image_annotations['query']

        if tags is None:
            tags = []

        terms = tags

        if text is not None and len(text) > 0:
            terms += string_to_concepts(text)

        if query is not None and len(query) > 0:
            terms += string_to_concepts(query)

        if len(terms) > 0:
            for term in terms:
                if term in concepts:
                    concepts[term] += 1
                else:
                    concepts[term] = 1

    sorted_concepts = sorted(concepts.items(), key=lambda x: x[1], reverse=True)
    print(sorted_concepts)

    terms = [x[0] for x in sorted_concepts]
    scores = [x[1] for x in sorted_concepts]

    plt.bar(range(len(terms)), scores, color='green', alpha=1)
    plt.xlabel('Terms')
    plt.ylabel('Frequency')
    plt.title('Term Frequency of Annotations')
    plt.legend()

    plt.show()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Analyse exported annotations')
    argparser.add_argument('input_file', help='The name of the json file to read')
    args = argparser.parse_args()

    analyse(args.input_file)
