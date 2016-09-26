"""
generate tables and graphs for use in latex

Harry Scells
September 2016
"""

import os
import pg8000
import sys


def annotators_table():
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
        'SELECT count(DISTINCT id) FROM annotated_assessment_images;'
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


if __name__ == '__main__':
    print(annotators_table())
