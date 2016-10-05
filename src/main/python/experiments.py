# python3

import os, sys, json, argparse, requests
from xml.dom import minidom


def run_experiments(topics_file, fields):
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

    r = requests.post('http://localhost:8080/api/eval/query', json=experiment)

    return r.text

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Export annotations from database')
    argparser.add_argument('topics', help='A topics.xml file distributed by NTCIR')
    argparser.add_argument('fields', help='The fields to run in the query', action='append',
                           choices=['text', 'tags', 'query', 'assessment'])
    argparser.add_argument('output', help='The file to write the trec run to',
                           default=sys.stdin, type=argparse.FileType('r'))
    args = argparser.parse_args()

    print(args)

    args.output.write(run_experiments(args.topics))
