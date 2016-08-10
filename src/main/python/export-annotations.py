# python3

import os, pg8000, sys, json, argparse


def export_json(output_file):
    if os.environ.get('LIFELOG_DB_USER') is None or \
                    os.environ.get('LIFELOG_DB_PASS') is None or \
                    os.environ.get('LIFELOG_DB_HOST') is None or \
                    os.environ.get('LIFELOG_DB_NAME') is None:
        print('Environment variables are not set!')
        sys.exit(1)

    conn = pg8000.connect(user=os.environ.get('LIFELOG_DB_USER'),
                          password=os.environ.get('LIFELOG_DB_PASS'),
                          host=os.environ.get('LIFELOG_DB_HOST'),
                          database=os.environ.get('LIFELOG_DB_NAME'))
    cursor = conn.cursor()

    with open(os.path.dirname(os.path.abspath(__file__)) + '/sql/export-annotations.sql',
              'r') as f:
        sql = f.read()
        cursor.execute(sql)

    results = cursor.fetchall()
    data = []
    for row in results:
        image_id, text, query, tags, assessment_annotations, assessment_relevences = row
        if assessment_annotations is not None:
            assessment = dict(zip(assessment_annotations, assessment_relevences))
        else:
            assessment = None
        data.append({'id': image_id, 'annotations': {'text': text, 'tags': tags, 'query': query,
                     'assessments': assessment}})

    cursor.close()
    with open(output_file, 'w') as f:
        f.write(json.dumps(data, sort_keys=False, indent=2, separators=(',', ': ')))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Export annotations from database')
    argparser.add_argument('output_file', help='The name of the file to output to')
    args = argparser.parse_args()

    export_json(args.output_file)
