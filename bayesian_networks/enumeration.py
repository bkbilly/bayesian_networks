#!/usr/bin/env python3

import copy
from bayesian_networks.bayesian import ParseInputs
from datetime import datetime

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


class BayesianClass():
    def __init__(self):
        pass

    def normalize(self, prob_results):
        normalized = []
        mysum = sum(item['prob'] for item in prob_results)
        for item in prob_results:
            if mysum != 0:
                item['norm'] = item['prob'] / mysum
            else:
                item['norm'] = 0
            normalized.append(item)
        return normalized

    def calc_query(self, node, query, graph):
        if len(self.graph[node]['parents']) == 0:
            prob = self.graph[node]['prob']
        else:
            # get the value of parents of node
            parents = tuple(query[par]
                            for par in self.graph[node]['parents'])
            prob = graph[node]['condition'][parents]

        if not query[node]:
            prob = round(1 - prob, 10)

        return prob


class Enumeration(BayesianClass):

    def __init__(self, graph=None):
        self.graph = graph

    def run(self, testcase):
        # Initialize graph
        parser = ParseInputs()
        known_data = parser.get_test_data(testcase['netid'])
        self.graph = parser.get_graph(known_data)
        node, query = parser.get_query('|'.join(testcase['query']))

        timer_start = datetime.now()
        enum_results = self.enum_ask(node, query)
        timediff = datetime.now() - timer_start

        normalized = {}
        unnormalized = {}
        for enum_result in enum_results:
            unnormalized[enum_result['condition']] = enum_result['prob']
            normalized[enum_result['condition']] = enum_result['norm']
        run_result = {
            'unnormalized': unnormalized,
            'normalized': normalized,
            'timediff': timediff,
            'too_much_wrong': False,
            'percWrong': False,
        }
        return run_result

    def enum_ask(self, node, query):
        sorted_nodes = list(self.graph.keys())
        prob_results = []
        for cond in [False, True]:
            query_copy = copy.deepcopy(query)
            query_copy[node] = cond

            # print(node, query_copy, cond)
            prob = self.enum_all(sorted_nodes, query_copy)
            prob_results.append({'condition': cond, 'prob': prob})

        return self.normalize(prob_results)

    def enum_all(self, sorted_nodes, query):
        if len(sorted_nodes) == 0:
            return 1.0
        if sorted_nodes[0] in query:
            ret = self.calc_query(
                sorted_nodes[0], query, self.graph) * self.enum_all(sorted_nodes[1:], query)
        else:
            probs = []
            query_copy = copy.deepcopy(query)
            for cond in [True, False]:
                query_copy[sorted_nodes[0]] = cond
                probs.append(self.calc_query(sorted_nodes[0], query_copy, self.graph) *
                             self.enum_all(sorted_nodes[1:], query_copy))
            ret = sum(probs)

        # print("%-14s | %-20s = %.8f" % (
        #     ' '.join(sorted_nodes),
        #     ' '.join('%s=%s' % (v, 't' if query[v] else 'f') for v in query),
        #     ret
        # ))
        return ret


if __name__ == '__main__':
    testcase = {
        'netid': "burglary",
        'query': ('B', 'j,m'),
        'result': {True: 0.28, False: 0.72},
    }
    Enumeration().run(testcase)
