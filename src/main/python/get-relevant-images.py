"""
Read the qrels file and get only the relevant images for use in annotation later

Harry Scells
September 2016
"""

import argparse


def parse_image(image_path):
    return image_path.split('/')[-1].replace('.jpg', '')


def extract_images(qrel_file, max_images=50):
    with open(qrel_file, 'r') as f:
        qrels = f.read().split('\n')

    images = set()
    qrel_count = {}
    for line in qrels:
        qrel_id, _, image, relevant = line.split(' ')
        if qrel_id not in qrel_count.keys():
            qrel_count[qrel_id] = 0
        if relevant == '1' and (qrel_count[qrel_id] < max_images or max_images < 0):
            qrel_count[qrel_id] += 1
            images.add(parse_image(image))

    return images


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('qrel', help='The qrel file')
    argparser.add_argument('output', help='The file to output to')

    args = argparser.parse_args()
    image_list = extract_images(args.qrel, max_images=-1)
    with open(args.output, 'w') as f:
        f.write('\n'.join(image_list))
