"""
generate tables and graphs for use in latex

Harry Scells
September 2016
"""

import os
import pg8000
import sys
import argparse


def annotators_table(cursor):
    """
    Create a LaTeX table containing the totals of the number of images annotated
    :param cursor:
    :return:
    """
    table_start = '''
\\begin{center}
    \\begin{tabular}{ | l | l | l | p{5cm} |}
    \hline
    Text & Tags & Query & Relevance Assessment \\\\ \hline
    '''
    table_end = '''
    \end{tabular}
\end{center}
    '''

    queries = [
        'SELECT count(id) FROM annotated_text_images;',
        'SELECT count(id) FROM annotated_tag_images;',
        'SELECT count(id) FROM annotated_query_images;',
        'SELECT count(DISTINCT image_id) FROM annotated_assessment_images;'
    ]

    query_results = []

    for query in queries:
        cursor.execute(query)
        result = cursor.fetchone()[0]
        query_results.append(result)

    return '{0}{1}{2}'.format(table_start,
                              '{} & {} & {} & {} \\\\ \hline'.format(query_results[0],
                                                                     query_results[1],
                                                                     query_results[2],
                                                                     query_results[3]),
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

    conn.close()
