"""
Plot the loss history from the output on neuraltalk2

Harry Scells
October 2016
"""

import argparse
import json
import matplotlib.pyplot as plt
from collections import OrderedDict
from operator import itemgetter


def plot_val_loss_history(files):
    """

    :param files:
    :return:
    """
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.title('Validation Loss History')

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            val_loss_history = data['val_loss_history']
            d = OrderedDict(sorted([(int(k), v) for k, v in val_loss_history.items()],
                                   key=itemgetter(0)))
            plt.plot([str(x) for x in d.keys()], list(d.values()),
                     label=file.split('.')[0].split('/')[-1])

    plt.legend(loc='best')
    plt.savefig('validation_loss_history.pdf', bbox_inches='tight')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('files', help='history files of the models',
                           type=str, nargs='+')

    args = argparser.parse_args()
    plot_val_loss_history(args.files)
