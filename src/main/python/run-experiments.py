# python3

import os, sys, json, argparse, requests
from xml.dom import minidom

# TODO: This should run an experiment for more than just the textual annotation type
def run_experiments(topics_file, output_file):
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
    experiment['fields'] = ['text', 'tags', 'query', 'assessment']

    r = requests.post('http://localhost:8080/api/eval/query', json=experiment)

    with open(output_file, 'w') as f:
        f.write(r.text)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Export annotations from database')
    argparser.add_argument('topics', help='A topics.xml file distributed by NTCIR')
    argparser.add_argument('output', help='The file to write the trec run to')
    args = argparser.parse_args()

    run_experiments(args.topics, args.output)
