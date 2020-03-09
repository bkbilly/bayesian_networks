#!/usr/bin/env python3

import bayesian_networks


if __name__ == "__main__":
    testcases = [
        # {
        #     'netid': "burglary",
        #     'query': ('B', 'j,m'),
        #     'result': {True: 0.28, False: 0.72},
        #     'samples': 10000,
        # },
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
        {
            'netid': "disease",
            'query': ('D', '+t'),
            'result': {True: 0.9, False: 0.1},
            'samples': 10000,
        },
        # {
        #     'netid': {
        #         'P(D)': 0.1,
        #         'P(T|d)': 0.99,
        #         'P(T|-d)': 0.05,
        #     },
        #     'query': ('D', '+t'),
        #     'result': {True: 0.7, False: 0.3},
        #     'samples': 10000,
        # },
        {
            'netid': "cancer",
            'query': ('S', '+co,+f'),
            'result': {True: 0.8, False: 0.2},
            'samples': 10000,
        },
    ]
    showcolors = True

    if not showcolors:
        for color in bayesian_networks.colors.keys():
            bayesian_networks.colors[color] = ''

    for testcase in testcases:
        myquery = 'P({}|{})'.format(testcase['query'][0], testcase['query'][1])
        print('{} {} - {} {}'.format(
            bayesian_networks.colors['WARNING'],
            testcase['netid'],
            myquery,
            bayesian_networks.colors['ENDC'])
        )

        print(bayesian_networks.colors['HEADER'] + '--> Enumeration' + bayesian_networks.colors['ENDC'])
        enum = bayesian_networks.Enumeration()
        bayesian_networks.print_result(enum.run(testcase), showcolors=showcolors)

        print(bayesian_networks.colors['HEADER'] + '--> RejectionSampling' + bayesian_networks.colors['ENDC'])
        rejection = bayesian_networks.RejectionSampling()
        bayesian_networks.print_result(rejection.run(testcase), showcolors=showcolors)

        print(bayesian_networks.colors['HEADER'] + '--> LikelihoodWeighting' + bayesian_networks.colors['ENDC'])
        weighting = bayesian_networks.LikelihoodWeighting()
        bayesian_networks.print_result(weighting.run(testcase), showcolors=showcolors)
