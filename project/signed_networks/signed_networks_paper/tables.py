#Implementation of tables listed in paper http://www.cs.cornell.edu/home/kleinber/chi10-signed.pdf
from itertools import combinations
from random import uniform
import numpy
from project import countries
from project.export_data.strongties import number_of_traids, __matrix_cube, get_relationship_matrix
from project.signed_networks.definitions import NO_LINK, NEGATIVE_LINK, POSITIVE_LINK
from project.util import memoize, std_dev

def table1(data, year, definition, def_args):
    def link_exists_def(data, year, A, B, def_args1):
        if 'World' in [A, B]: return 0
        return 0 if definition(data, year, A, B, def_args) == NO_LINK else 1

    positive_edges_count, negative_edges_count, no_edge_count, traids = 0, 0, 0, 0
    for (A, B) in countries.country_pairs(data.countries()):
        link_type = definition(data, year, A, B, def_args)
        if link_type == NEGATIVE_LINK: negative_edges_count += 1
        elif link_type == POSITIVE_LINK: positive_edges_count += 1
        elif link_type == NO_LINK: no_edge_count += 1

    edges_count = positive_edges_count + negative_edges_count
    return {'Name': 'Table1',
            'Nodes': len(data.countries()),
            'Edges': edges_count,
            '+ edges': positive_edges_count * 100.0 / edges_count,
            '- edges': negative_edges_count * 100.0 / edges_count,
            'Traids': number_of_traids(__matrix_cube(get_relationship_matrix(data, year, link_exists_def, {})))
    }


def table2(data, year, definition, def_args):
    class RandomLinkGenerator:
        def __init__(self, positive, negative):
            self.total_positive = positive
            self.total_negative = negative

            self.assigned_positive = 0
            self.assigned_negative = 0

        def __random_pick(self, list, probabilities):
            x = uniform(0, 1)
            cumulative_probability = 0.0
            for item, item_probability in zip(list, probabilities):
                cumulative_probability += item_probability
                if x < cumulative_probability: break
            return item

        @memoize
        def next_random(self, pair):
            # argument 'pair' is used for memoization
            remaining_positive = self.total_positive - self.assigned_positive
            remaining_negative = self.total_negative - self.assigned_negative
            total_remaining = remaining_positive + remaining_negative
            retval = self.__random_pick([POSITIVE_LINK, NEGATIVE_LINK],
                [1.0 * remaining_positive / total_remaining, 1.0 * remaining_negative / total_remaining])
            if retval == POSITIVE_LINK: self.assigned_positive += 1
            if retval == NEGATIVE_LINK: self.assigned_negative += 1
            return retval

    t0, t1, t2, t3 = 0, 0, 0, 0
    total_positive, total_negative, total_missing = 0, 0, 0
    traids = []
    for (A, B, C) in combinations(data.countries(), 3):
        side1 = definition(data, year, A, B, def_args)
        side2 = definition(data, year, B, C, def_args)
        side3 = definition(data, year, C, A, def_args)

        if side1 == NO_LINK or side2 == NO_LINK or side3 == NO_LINK: continue
        traids.append((A, B, C))
        for side in [side1, side2, side3]:
            if side == POSITIVE_LINK: total_positive += 1
            if side == NEGATIVE_LINK: total_negative += 1

        positive_sides = 0
        for side in [side1, side2, side3]:
            if side == POSITIVE_LINK: positive_sides += 1
        if positive_sides == 0: t0 += 1
        if positive_sides == 1: t1 += 1
        if positive_sides == 2: t2 += 1
        if positive_sides == 3: t3 += 1
    total = t0 + t1 + t2 + t3

    rt0, rt1, rt2, rt3, rtotal = [], [], [], [], []
    MAX_RANDOM_RUNS = 5
    for i in range(0, MAX_RANDOM_RUNS):
        for list in [rt0, rt1, rt2, rt3, rtotal]: list.append(0)

        r = RandomLinkGenerator(total_positive, total_negative)
        for (A, B, C) in traids:
            positive_sides = 0
            side1 = r.next_random(sorted([A, B]))
            side2 = r.next_random(sorted([B, C]))
            side3 = r.next_random(sorted([C, A]))
            for side in [side1, side2, side3]:
                if side == POSITIVE_LINK: positive_sides += 1
            if positive_sides == 0: rt0[i] += 1
            if positive_sides == 1: rt1[i] += 1
            if positive_sides == 2: rt2[i] += 1
            if positive_sides == 3: rt3[i] += 1
        rtotal[i] = rt0[i] + rt1[i] + rt2[i] + rt3[i]


    def table2_row(t0, total, rt0, rtotal):
        def pTi(t, total): return t * 1.0 / total

        def sTi(rt0, rtotal, t0): return 99999999 if rt0 == 0 else (t0 - rt0) / (
            pow(rt0 * (1 - rt0 * 1.0 / rtotal), 0.5))

        return {'|Ti|': t0,
                'p(Ti)': pTi(t0, total),
                'p0(Ti)': numpy.mean([pTi(rt0[i], rtotal[i]) for i in range(0, MAX_RANDOM_RUNS)]),
                'p0(Ti)-sd': std_dev([pTi(rt0[i], rtotal[i]) for i in range(0, MAX_RANDOM_RUNS)]),
                's(Ti)': numpy.mean([sTi(rt0[i], rtotal[i], t0) for i in range(0, MAX_RANDOM_RUNS)]),
                's(Ti)-sd': std_dev([sTi(rt0[i], rtotal[i], t0) for i in range(0, MAX_RANDOM_RUNS)])
        }

    return {'Name': 'Table2',
            'T0': table2_row(t0, total, rt0, rtotal),
            'T1': table2_row(t1, total, rt1, rtotal),
            'T2': table2_row(t2, total, rt2, rtotal),
            'T3': table2_row(t3, total, rt3, rtotal)}
