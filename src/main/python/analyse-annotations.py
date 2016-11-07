# python3

import argparse, json, re, operator, math, os
import matplotlib.pyplot as plt
import numpy as np
from autocorrect import spell
from xml.dom import minidom

concepts_regex = re.compile(r'[^a-zA-Z0-9-]+')


def string_to_concepts(string):
    return concepts_regex.sub(' ', string).lower().strip().split(' ')


def extract_terms(annotation):
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

    return terms


# http://stackoverflow.com/questions/12418234/logarithmically-spaced-integers
def gen_log_space(limit, n):
    result = [1]
    if n>1:  # just a check to avoid ZeroDivisionError
        ratio = (float(limit)/result[-1]) ** (1.0/(n-len(result)))
    while len(result)<n:
        next_value = result[-1]*ratio
        if next_value - result[-1] >= 1:
            # safe zone. next_value will be a different integer
            result.append(next_value)
        else:
            # problem! same integer. we need to find next_value by artificially
            # incrementing previous value
            result.append(result[-1]+1)
            # recalculate the ratio so that the remaining values will scale correctly
            ratio = (float(limit)/result[-1]) ** (1.0/(n-len(result)))
    # round, re-adjust to 0 indexing (i.e. minus 1) and return np.uint64 array
    return np.array([round(x)-1 for x in result], dtype=np.uint64)


def tf(input_file):

    concepts = {}

    with open(input_file) as f:
        annotations = json.loads(f.read())

    for annotation in annotations:
        terms = extract_terms(annotation)
        if len(terms) > 0:
            for term in terms:
                if term in concepts:
                    concepts[term] += 1
                else:
                    concepts[term] = 1

    return concepts


def idf(input_file):
    documents = {}
    terms = set()
    concepts = {}
    scores = {}

    with open(input_file) as f:
        annotations = json.loads(f.read())

    for annotation in annotations:
        terms = terms | set(extract_terms(annotation))
        documents[annotation['id']] = set(extract_terms(annotation))

    for term in terms:
        for document in documents.values():
            if term in concepts and term in document:
                concepts[term] += 1
            elif term in document:
                concepts[term] = 1

    N = len(documents)

    for term in concepts:
        scores[term] = math.log(1 + (N/concepts[term]), 10)

    return scores


def tfidf(input_file):
    tf_scores = tf(input_file)
    idf_scores = idf(input_file)

    scores = {}

    for term in tf_scores:
        score = tf_scores[term] * idf_scores[term]
        scores[term] = score

    return scores


def display_scores(scores, title='title', xlabel='x', ylabel='y', filename='scores.pdf'):
    sorted_concepts = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    terms = [x[0] for x in sorted_concepts]
    scores = [x[1] for x in sorted_concepts]

    print(len(terms))

    fig, ax = plt.subplots()
    plt.xticks(range(len(terms)), terms, rotation='vertical')
    ax.semilogy(range(len(scores)), scores, color='blue', alpha=1)
    ax.locator_params(nbins=40, axis='x')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()

    plt.savefig(filename, bbox_inches='tight')


def sample(scores, topics_file='lifelog_qrels/lifelogging_topics_formal.xml', max=50):

    xmldoc = minidom.parse(topics_file)
    topic_nodes = xmldoc.getElementsByTagName('topic')

    queries = ""

    for node in topic_nodes:
        topic = {}
        for tag in node.childNodes:
            if tag.nodeType == tag.ELEMENT_NODE:
                name, value = tag.tagName, tag.childNodes[0].nodeValue
                if name == 'narrative':
                    queries += value

    query_terms = set(string_to_concepts(queries))
    topics = []

    concepts = {}
    terms = []

    with open(os.path.dirname(os.path.abspath(__file__)) + '/data/stopwords.txt') as f:
        stopwords = f.read().split('\n')

    for term in query_terms:
        if term not in stopwords:
            topics.append(term)

    for term in scores:
        if term not in stopwords and term in topics:
            concepts[term] = scores[term]

    sorted_concepts = sorted(concepts.items(), key=lambda x: x[1], reverse=True)

    sorted_terms = [x[0] for x in sorted_concepts]

    indices = gen_log_space(len(sorted_terms), max)
    for i in indices:
        terms.append(sorted_terms[i])

    for i in range(len(terms)):
        terms[i] = spell(terms[i]).lower()
    print(terms, len(terms))

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Analyse exported annotations')
    argparser.add_argument('input_file', help='The name of the json file to read')
    args = argparser.parse_args()

    display_scores(idf(args.input_file), title='Inverse Document Frequency of annotations',
                   xlabel='Terms', ylabel='Scores', filename='idf-scores.pdf')
    display_scores(tf(args.input_file), title='Term Frequency of annotations', xlabel='Terms',
                   ylabel='Scores', filename='tf-scores.pdf')
