"""
Process the qrels file to work with evaluation

Harry Scells
"""

import argparse


def process(qrels_file):
    """
    read a qrel file and process it for use in evaluation
    :return:
    """
    with open(qrels_file, 'r') as f:
        for line in f.readlines():
            topic_id, q0, image_path, relevance = line.split(' ')
            image_id = image_path.split('/')[-1].replace('.jpg', '')
            print('{} {} {} {}'.format(topic_id, q0, image_id, relevance.replace('\n', '')))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('qrels_file', help='The qrels file to load')

    args = argparser.parse_args()

    process(args.qrels_file)