"""
generate tables and graphs for use in latex

Harry Scells
September 2016
"""

import os
import pg8000
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np


def format_time(td):
    d, h, m = td.days, td.seconds // 3600, (td.seconds // 60) % 60
    if d > 0:
        return '{} days, {} hours'.format(d, h)
    elif h == 1:
        return '{} hour, {} minutes'.format(h, m)
    elif h > 1:
        return '{} hours, {} minutes'.format(h, m)
    elif m == 1:
        return '{} minute'.format(m)
    elif m > 1:
        return '{} minutes'.format(m)
    return '{} seconds'.format(td.seconds)


def annotators_breakdown(cursor, file):
    """

    :param cursor:
    :param file:
    :return:
    """
    sql = '''
SELECT row_number() OVER() AS annotator, sum(
    (SELECT count(DISTINCT image_id) FROM annotated_text_images WHERE person_id = p.id) +
    (SELECT count(DISTINCT image_id) FROM annotated_tag_images WHERE person_id = p.id) +
    (SELECT count(DISTINCT image_id) FROM annotated_query_images WHERE person_id = p.id) +
    (SELECT count(DISTINCT image_id) FROM annotated_assessment_images WHERE person_id = p.id)
) total
FROM people p
GROUP BY p.alias
ORDER BY total DESC;
    '''

    cursor.execute(sql)
    results = cursor.fetchall()
    count = []
    total = 0
    for row in results:
        if row[1] > 0:
            total += row[1]
            count.append(row[1])

    ind = np.arange(len(count))
    width = 1.0
    fig, ax = plt.subplots()
    rects = ax.bar(ind, count, width)
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height,
                '%d' % int(height),
                ha='center', va='bottom')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(ind + 1, minor=False)
    plt.title('Annotation Count Breakdown')
    plt.xlabel('Annotator (anonymised)')
    plt.ylabel('Number of annotations')
    plt.savefig(file)
    return total


def relevant_images_count(cursor, file):
    """

    :param cursor:
    :param file:
    :return:
    """
    sql = 'SELECT topic_id, count(image_id) ' \
          'FROM images_topics ' \
          'GROUP BY topic_id ' \
          'ORDER BY topic_id;'

    cursor.execute(sql)
    results = cursor.fetchall()
    topics = {}
    total = 0
    for row in results:
        topics[row[0]] = row[1]

    ind = np.arange(len(topics) + 1)[1:]
    width = 1.0
    fig, ax = plt.subplots()
    rects = ax.bar(topics.keys(), topics.values(), width)
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height+10,
                '%d' % int(height),
                ha='center', va='bottom', rotation='vertical', fontsize='smaller')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(ind, minor=False, rotation='vertical', fontsize='smaller')
    plt.title('Number of Relevant Images Per Topic')
    plt.xlabel('Topic Id')
    plt.ylabel('Relevant Images')
    plt.savefig(file)
    return total


def annotators_table(cursor):
    """
    Create a LaTeX table containing the totals of the number of images annotated
    :param cursor:
    :return:
    """
    table_start = '''
\\begin{center}
    \\begin{tabular}{ | l | l | l | l | p{5cm} |}
    \hline
    Name & Count & Average Time & Total Time \\\\ \hline
    '''
    table_end = '''
    \end{tabular}
\end{center}
    '''

    queries = [
        ('Text', 'SELECT count(id), avg(end_time - start_time), sum(end_time - start_time) '
                 'FROM annotated_text_images;'),
        ('Tag', 'SELECT count(id), avg(end_time - start_time), sum(end_time - start_time) '
                'FROM annotated_tag_images;'),
        ('Query', 'SELECT count(id), avg(end_time - start_time), sum(end_time - start_time) '
                  'FROM annotated_query_images;'),
        ('Assessment', '''SELECT count(DISTINCT image_id), avg(a.end_time - a.start_time), q.z
                          FROM annotated_assessment_images a,
                           (SELECT DISTINCT sum(x.y) z FROM
                            (SELECT DISTINCT image_id, avg(end_time - start_time) y
                             FROM annotated_assessment_images GROUP BY image_id) x) q
                          GROUP BY q.z;''')
    ]

    query_results = []
    total_count, total_time = 0, 0
    for name, query in queries:
        cursor.execute(query)
        result = cursor.fetchone()
        query_results.append((name, format_time(result[1]), result[0], format_time(result[2])))

    print(query_results)

    return '{}{}{}'.format(table_start,
                           '\n    '.join(['{} & {} & {} & {} \\\\ \hline'.format(a, c, b, d)
                                          for (a, b, c, d) in
                                          query_results]),
                           table_end)


def trec_eval_table(results):
    """
    Create a LaTeX table containing the the results from running trec_eval
    :param results:
    :return:
    """
    # process the trec results file
    results = [x.split('\t') for x in [''.join(x.split(' ')) for x in results.split('\n')]]

    # filter the results down to just the 'all' labels
    all_results = list(filter(lambda x: len(x) == 3 and x[1] == 'all', results))

    table_start = '''
\\begin{center}
    \\begin{tabular}{ | l | l | }
    \hline
    Metric & Score \\\\ \hline
'''
    table_end = '''
    \end{tabular}
\end{center}
'''

    return '{0}{1}{2}'.format(table_start,
                              '\n'.join(
                                  ['\t{} & {} \\\\ \hline'.format(x[0], x[2]).replace('_', '\_')
                                   for x in
                                   all_results[1:]]),
                              table_end)


def run_arg(result, comment=''):
    print('% {}'.format(comment))
    print(result)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--annotations_table',
                           help='table showing the number of annotations',
                           required=False, default=False, type=bool)
    argparser.add_argument('--annotator_breakdown',
                           help='table showing the number of annotations',
                           required=False, default=None, type=str)
    argparser.add_argument('--relevant_images',
                           help='plot the relevant images',
                           required=False, default=None, type=str)
    argparser.add_argument('--trec_eval_results',
                           help='table showing a trec_eval results',
                           required=False, type=argparse.FileType('r'))

    args = argparser.parse_args()

    if os.environ.get('LIFELOG_DB_USER') is None or \
       os.environ.get('LIFELOG_DB_PASS') is None or \
       os.environ.get('LIFELOG_DB_HOST') is None or \
       os.environ.get('LIFELOG_DB_NAME') is None:
        print('Environment variables are not set!')
        sys.exit(1)

    if len(sys.argv[1:]) < 1:
        argparser.print_help()
        argparser.exit()

    conn = pg8000.connect(user=os.environ.get('LIFELOG_DB_USER'),
                          password=os.environ.get('LIFELOG_DB_PASS'),
                          host=os.environ.get('LIFELOG_DB_HOST'),
                          database=os.environ.get('LIFELOG_DB_NAME'))
    cursor = conn.cursor()

    if args.annotations_table:
        run_arg(annotators_table(cursor), 'annotations table')
    if args.trec_eval_results is not None:
        run_arg(trec_eval_table(args.trec_eval_results.read()), 'trec_eval results')
    if args.annotator_breakdown is not None:
        run_arg(annotators_breakdown(cursor, args.annotator_breakdown), 'annotator breakdown')
    if args.relevant_images is not None:
        run_arg(relevant_images_count(cursor, args.relevant_images), 'relevant images')

    conn.close()
