#!/usr/bin/env python3

import random
from bayesian_networks.bayesian import ParseInputs
import logging
from datetime import datetime


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

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


class ApproximateInference():
    """docstring for ApproximateInference"""
    def __init__(self):
        pass

    def run(self, testcase):
        if 'samples' not in testcase:
            self.samples = 10000
        else:
            self.samples = testcase['samples']
        if self.samples <= 5 and self.samples is not None:
            logger.setLevel(logging.DEBUG)
        # Initialize graph
        parser = ParseInputs()
        known_data = parser.get_test_data(testcase['netid'])
        self.graph = parser.get_graph(known_data)

        node, query = parser.get_query('|'.join(testcase['query']))

        # Test with my data graph
        timer_start = datetime.now()
        unnormalized = self.start_inference(node, query)
        normalized = self.normalize(unnormalized)
        timediff = datetime.now() - timer_start

        percWrong = {}
        too_much_wrong = False
        for key in normalized.keys():
            percWrong[key] = round(abs(normalized[key] - testcase['result'][key]), 3)
            if percWrong[key] >= 0.1:
                too_much_wrong = True
        run_result = {
            'unnormalized': unnormalized,
            'normalized': normalized,
            'timediff': timediff,
            'too_much_wrong': too_much_wrong,
            'percWrong': percWrong,
        }
        return run_result

    def get_probability(self, node, conditions):
        prob = self.graph[node]['prob']
        if prob is None:
            conditional = []
            for par in self.graph[node]['parents']:
                conditional.append(conditions[par]['value'])
            conditional = tuple(conditional)
            if conditional in self.graph[node]['condition']:
                prob = self.graph[node]['condition'][conditional]

        return prob

    def random_sample(self, node, prob):
        randnumber = random.random()  # between 0 and 1

        retNode = True
        if prob is not None and randnumber > prob:
            retNode = False

        return retNode

    def normalize(self, prob_results):
        normalized = {}
        mysum = float(sum(prob_results.values()))
        for cond, value in prob_results.items():
            if mysum != 0:
                normalized[cond] = value / mysum
            else:
                normalized[cond] = 0
        return normalized

    def get_conditions(self, query, keepquery=False):
        logger.debug('----------============-----------')
        conditions = {
            key: {'value': None, 'prob': 1}
            for key in self.graph.keys()
        }

        for node, node_options in self.graph.items():
            logger.debug('--==' + node + '==--')
            if node in query:
                logger.debug(" exists in query")
                prob = self.get_probability(node, conditions)
                if keepquery:
                    rand = self.random_sample(node, prob)
                    conditions[node]['value'] = query[node] == rand
                else:
                    conditions[node]['value'] = query[node]
                conditions[node]['prob'] = prob
            else:
                logger.debug(' conditional')
                prob = self.get_probability(node, conditions)
                rand = self.random_sample(node, prob)
                conditions[node]['value'] = rand

        return conditions


class RejectionSampling(ApproximateInference):

    def __init__(self, graph=None, samples=None, showcolors=False):
        if not showcolors:
            for color in colors.keys():
                colors[color] = ''

        self.graph = graph
        self.samples = samples
        if self.samples is not None and self.samples <= 5:
            logger.setLevel(logging.DEBUG)

    def start_inference(self, node, query):
        ''' rejection_sampling '''
        likelihood = {False: 0, True: 0}
        for num, sample in enumerate(range(self.samples)):
            sampVars = self.prior_sampling(query)
            existsinQuery = all(
                sampVars[q_node]['value'] == q_value
                for q_node, q_value in query.items()
            )
            if existsinQuery:
                if sampVars[node]['value']:
                    likelihood[True] += 1
                else:
                    likelihood[False] += 1

        return likelihood

    def prior_sampling(self, query):
        conditions = self.get_conditions(query, True)

        logger.debug('\n')
        logger.debug('conditions: ' + str(conditions))
        logger.debug('\n')

        return conditions


class LikelihoodWeighting(ApproximateInference):

    def __init__(self, graph=None, samples=None, showcolors=False):
        if not showcolors:
            for color in colors.keys():
                colors[color] = ''

        self.graph = graph
        self.samples = samples
        if self.samples is not None and self.samples <= 5:
            logger.setLevel(logging.DEBUG)

    def start_inference(self, node, query):
        ''' weighted_likelihood '''
        likelihood = {False: 0, True: 0}
        for num, sample in enumerate(range(self.samples)):
            event, weight = self.weighted_sample(query)
            likelihood[event[node]['value']] += weight

        likelihood[False] = likelihood[False]
        likelihood[True] = likelihood[True]
        return likelihood

    def weighted_sample(self, query):
        conditions = self.get_conditions(query, False)
        weight = 1
        for node, condition in conditions.items():
            if condition['prob'] != 1 and condition['prob'] is not None:
                if not condition['value']:
                    condition['prob'] = 1 - condition['prob']
                weight *= condition['prob']

        logger.debug('\n')
        logger.debug('conditions: ' + str(conditions))
        logger.debug('weight: ' + str(weight))
        logger.debug('\n')

        return conditions, weight


if __name__ == "__main__":

    testcases = [
        {
            'netid': "burglary",
            'query': ('A', 'b,e'),
            'result': {True: 0.95, False: 0.05},
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
    showcolors = True

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

        print(colors['HEADER'] + '--> RejectionSampling' + colors['ENDC'])
        RejectionSampling().run(testcase)

        print(colors['HEADER'] + '--> LikelihoodWeighting' + colors['ENDC'])
        LikelihoodWeighting().run(testcase)
