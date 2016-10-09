# python3

import argparse
import requests
import sys
from xml.dom import minidom


def run_experiments(topics_file, fields=None, experiment_name='annotation'):
    if fields is None:
        fields = ['text', 'tags', 'query', 'assessment']

    xmldoc = minidom.parse(topics_file)
    topic_nodes = xmldoc.getElementsByTagName('topic')

    experiment = {}
    topics = []

    for node in topic_nodes:
        topic = {}
        for tag in node.childNodes:
            if tag.nodeType == tag.ELEMENT_NODE:
                name, value = tag.tagName, tag.childNodes[0].nodeValue
                if name == 'id':
                    topic['queryId'] = value
                elif name == 'title':
                    topic['query'] = value
                elif name == 'description':
                    topic['description'] = value
        topics.append(topic)

    experiment['topics'] = topics
    experiment['fields'] = fields
    experiment['name'] = experiment_name

    r = requests.post('http://localhost:8080/api/eval/query', json=experiment)

    return r.text


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Export annotations from database')
    argparser.add_argument('-f', '--fields', help='The fields to run in the query',
                           action='append', choices=['text', 'tags', 'query', 'assessment'])
    argparser.add_argument('-o', '--output', help='The file to write the trec run to',
                           default=sys.stdout, type=argparse.FileType('w'), required=False)
    argparser.add_argument('-n', '--name', help='The name of the experiment',
                           default='annotation', type=str, required=False)
    argparser.add_argument('topics', help='A topics.xml file distributed by NTCIR')

    args = argparser.parse_args()

    args.output.write(run_experiments(args.topics, args.fields, args.name))
