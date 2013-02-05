#Implementation of tables listed in paper http://www.cs.cornell.edu/home/kleinber/chi10-signed.pdf
from itertools import combinations
from random import uniform
from project import countries
from project.export_data.strongties import number_of_traids, __matrix_cube, get_relationship_matrix
from project.signed_networks.definitions import NO_LINK, NEGATIVE_LINK, POSITIVE_LINK
from project.util import memoize

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
    rt0, rt1, rt2, rt3 = 0, 0, 0, 0
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

    r = RandomLinkGenerator(total_positive, total_negative)
    for (A, B, C) in traids:
        positive_sides = 0
        side1 = r.next_random(sorted([A, B]))
        side2 = r.next_random(sorted([B, C]))
        side3 = r.next_random(sorted([C, A]))
        for side in [side1, side2, side3]:
            if side == POSITIVE_LINK: positive_sides += 1
        if positive_sides == 0: rt0 += 1
        if positive_sides == 1: rt1 += 1
        if positive_sides == 2: rt2 += 1
        if positive_sides == 3: rt3 += 1
    rtotal = rt0 + rt1 + rt2 + rt3

    return {'Name': 'Table2',
            'T0': {'|Ti|': t0, 'p(Ti)': t0 * 1.0 / total, 'p0(Ti)': rt0 * 1.0 / rtotal,
                   's(Ti)': 99999999 if rt0 == 0 else (t0 - rt0) / (pow(rt0 * (1 - rt0 * 1.0 / rtotal), 0.5))},
            'T1': {'|Ti|': t1, 'p(Ti)': t1 * 1.0 / total, 'p0(Ti)': rt1 * 1.0 / rtotal,
                   's(Ti)': 99999999 if rt1 == 0 else(t1 - rt1) / (pow(rt1 * (1 - rt1 * 1.0 / rtotal), 0.5))},
            'T2': {'|Ti|': t2, 'p(Ti)': t2 * 1.0 / total, 'p0(Ti)': rt2 * 1.0 / rtotal,
                   's(Ti)': 99999999 if rt2 == 0 else(t2 - rt2) / (pow(rt2 * (1 - rt2 * 1.0 / rtotal), 0.5))},
            'T3': {'|Ti|': t3, 'p(Ti)': t3 * 1.0 / total, 'p0(Ti)': rt3 * 1.0 / rtotal,
                   's(Ti)': 99999999 if rt3 == 0 else(t3 - rt3) / (pow(rt3 * (1 - rt3 * 1.0 / rtotal), 0.5))}}