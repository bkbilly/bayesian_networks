#!/usr/bin/env python3

import bayesian_networks

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


if __name__ == "__main__":
    testcases = [
        {
            'netid': "burglary",
            'query': ('B', 'j,m'),
            'result': {True: 0.28, False: 0.72},
            'samples': 10000,
        },
        # {
        #     'netid': "sprinkler",
        #     'query': ('W', 's,-r'),
        #     'result': {True: 0.90, False: 0.10},
        #     'samples': 10000,
        # },
        # {
        #     'netid': "sprinkler",
        #     'query': ('R', 'c,s'),
        #     'result': {True: 0.80, False: 0.20},
        #     'samples': 10000,
        # },
        # {
        #     'netid': "sprinkler",
        #     'query': ('R', '-c,+w'),
        #     'result': {True: 0.35, False: 0.65},
        #     'samples': 10000,
        # },
        # {
        #     'netid': "disease",
        #     'query': ('D', '+t'),
        #     'result': {True: 0.7, False: 0.3},
        #     'samples': 10000,
        # },
        # {
        #     'netid': "cancer",
        #     'query': ('S', '+co,+f'),
        #     'result': {True: 0.8, False: 0.2},
        #     'samples': 10000,
        # },
    ]
    showcolors = False

    if not showcolors:
        for color in colors.keys():
            colors[color] = ''

    for testcase in testcases:
        myquery = 'P({}|{})'.format(testcase['query'][0], testcase['query'][1])
        print('{} {} - {} {}'.format(
            colors['WARNING'],
            testcase['netid'],
            myquery,
            colors['ENDC'])
        )

        # print(colors['HEADER'] + '--> Enumeration' + colors['ENDC'])
        # bayesian_networks.Enumeration().run(testcase)

        print(colors['HEADER'] + '--> RejectionSampling' + colors['ENDC'])
        bayesian_networks.RejectionSampling(showcolors=showcolors).run(testcase)

        print(colors['HEADER'] + '--> LikelihoodWeighting' + colors['ENDC'])
        bayesian_networks.LikelihoodWeighting(showcolors=showcolors).run(testcase)
