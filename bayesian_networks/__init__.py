#!/usr/bin/env python3

from bayesian_networks.enumeration import Enumeration
from bayesian_networks.approximate_inference import LikelihoodWeighting
from bayesian_networks.approximate_inference import RejectionSampling

colors = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}


def print_result(run_result, showcolors=False):
    unnormalized = {key: round(value, 5) for key, value in run_result['unnormalized'].items()}
    normalized = {key: round(value, 5) for key, value in run_result['normalized'].items()}
    print('  unnormalized: {}'.format(unnormalized))
    print('  Normalized: {}'.format(normalized))
    if run_result['too_much_wrong']:
        print('{} ! percent Wrong: {}{}'.format(
            colors['FAIL'],
            run_result['percWrong'],
            colors['ENDC'])
        )
    print('  time: {}'.format(run_result['timediff']))
