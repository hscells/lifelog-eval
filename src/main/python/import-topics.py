"""
Read the qrels file and get only the relevant images for use in annotation later

Harry Scells
September 2016
"""

import argparse
import os
import sys

import pg8000
import progressbar

import xml.etree.ElementTree as et
from collections import namedtuple

Topic = namedtuple('Topic', ['id', 'title', 'description', 'narrative'])


def import_topics(topics_file, qrels_file):
    if os.environ.get("LIFELOG_DB_USER") is None or \
                    os.environ.get("LIFELOG_DB_PASS") is None or \
                    os.environ.get("LIFELOG_DB_HOST") is None or \
                    os.environ.get("LIFELOG_DB_NAME") is None:
        print("Environment variables are not set!")
        sys.exit(1)

    topics = []
    topics_dom = et.parse(topics_file)
    for topic_el in topics_dom.iter('topic'):
        id, title, description, narrative = '', '' ,'' ,''
        for node in topic_el:
            if node.tag == 'id':
                id = node.text
            elif node.tag == 'title':
                title = node.text
            elif node.tag == 'description':
                description = node.text
            elif node.tag == 'narrative':
                narrative = node.text
        topics.append(Topic(id, title, description, narrative))

    print(topics)

    with open(qrels_file, 'r') as f:
        qrels = f.read().split('\n')

    images = {}
    for line in qrels:
        topic_id, _, image_path, relevance = line.split(' ')
        if relevance == '1':
            image = image_path.split('/')[-1].replace('.jpg', '')
            images[image] = topic_id

    conn = pg8000.connect(user=os.environ.get("LIFELOG_DB_USER"),
                          password=os.environ.get("LIFELOG_DB_PASS"),
                          host=os.environ.get("LIFELOG_DB_HOST"),
                          database=os.environ.get("LIFELOG_DB_NAME"))
    cursor = conn.cursor()

    with progressbar.ProgressBar(max_value=len(topics)) as bar:
        i = 0
        for topic in topics:
            cursor.execute('INSERT INTO topics (topic_id, title, description, narrative) '
                           'VALUES (%s, %s, %s, %s)',
                           [topic.id, topic.title, topic.description, topic.narrative])
            i += 1
            bar.update(i)

    with progressbar.ProgressBar(max_value=len(images)) as bar:
        i = 0
        for image_id, topic_id in images.items():
            cursor.execute('INSERT INTO images_topics (image_id, topic_id) '
                           'VALUES (%s, %s)',
                           [image_id, topic_id])
            i += 1
            bar.update(i)
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('topics', help='The file containing the topics')
    argparser.add_argument('qrels', help='The file containing the qrels')

    args = argparser.parse_args()
    import_topics(args.topics, args.qrels)
