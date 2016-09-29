"""
Read the qrels file and get only the relevant images for use in annotation later

Harry Scells
September 2016
"""

import argparse
import base64
import sys
import os

from PIL import Image
from io import BytesIO


def import_images(target_dir, images_file):
    if os.environ.get("LIFELOG_DB_USER") is None or \
                    os.environ.get("LIFELOG_DB_PASS") is None or \
                    os.environ.get("LIFELOG_DB_HOST") is None or \
                    os.environ.get("LIFELOG_DB_NAME") is None:
        print("Environment variables are not set!")
        sys.exit(1)

    with open(images_file, 'r') as f:
            images = f.read().split('\n')

    db_images = {}
    # walk each directory in the target directory
    for root, dirs, files in os.walk(target_dir):
        # walk each file in each one of the directories
        for file in files:
            for image_id in images:
                if image_id not in db_images.keys() and image_id in file:
                    with open(root + '/' + file, 'rb') as i:
                        image = Image.open(i)
                        (w, h) = image.size

                        image = image.resize((w / 2, h / 2), Image.ANTIALIAS)

                        buffer = BytesIO()
                        image.save(buffer, format='JPEG')

                        db_images[image_id] = base64.b64encode(buffer)

    print(db_images)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('target', help='Folder containing the images')
    argparser.add_argument('images', help='The list of image ids to import')

    args = argparser.parse_args()
    import_images(args.target, args.images)
