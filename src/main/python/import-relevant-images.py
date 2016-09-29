"""
Read the qrels file and get only the relevant images for use in annotation later

Harry Scells
September 2016
"""

import progressbar
import argparse
import base64
import pg8000
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
            # now we can check if the current file is one of the images to upload
            for image_id in images:
                # for performance we can use a dict
                if image_id not in db_images.keys() and image_id in file:
                    with open(root + '/' + file, 'rb') as i:
                        image = Image.open(i)
                        (w, h) = image.size

                        # we want to resize the image to save data
                        image = image.resize((int(w / 2), int(h / 2)), Image.ANTIALIAS)

                        buffer = BytesIO()
                        image.save(buffer, format='JPEG')

                        db_images[image_id] = base64.b64encode(buffer.getvalue())

    conn = pg8000.connect(user=os.environ.get("LIFELOG_DB_USER"),
                          password=os.environ.get("LIFELOG_DB_PASS"),
                          host=os.environ.get("LIFELOG_DB_HOST"),
                          database=os.environ.get("LIFELOG_DB_NAME"))
    cursor = conn.cursor()

    with progressbar.ProgressBar(max_value=len(db_images)) as bar:
        i = 0
        for image_id, image_data in db_images.items():
            cursor.execute('INSERT INTO images (name, data) VALUES (%s, %s)',
                           [image_id, image_data])
            i += 1
            bar.update(i)
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('target', help='Folder containing the images')
    argparser.add_argument('images', help='The list of image ids to import')

    args = argparser.parse_args()
    import_images(args.target, args.images)
