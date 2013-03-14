#Implementation of tables listed in paper http://www.cs.cornell.edu/home/kleinber/chi10-signed.pdf
from itertools import combinations
import numpy
from project import countries
from project.export_data.strongties import number_of_traids, __matrix_cube, get_relationship_matrix
from project.signed_networks.definitions import NO_LINK, NEGATIVE_LINK, POSITIVE_LINK
from project.signed_networks.structural_balance.metrics.util import RandomLinkGenerator
from project.util import std_dev, memoize


def print_table(json):
    print json['Name']
    if json['Name'] == 'Table1':
        print "%d\t%.2f\t%2f\t%d" % (json['Edges'], json['+ edges'], json['- edges'], json['Traids'])
    elif json['Name'] == 'Table2':
        for t in ['T3', 'T1', 'T2', 'T0']:
            r = json[t]
            print "%s| %d \t| %.3g \t| %.3g \t| %.3g \t| %.1f \t| %.1f \t|" % (
                t, r['|Ti|'], r['p(Ti)'], r['p0(Ti)'], r['p0(Ti)-sd'], r['s(Ti)'], r['s(Ti)-sd'])


@memoize
def sign_distributions(data, year, definition, def_args):
    positive_edges_count, negative_edges_count, no_edge_count = 0, 0, 0
    for (A, B) in countries.country_pairs(data.countries()):
        link_type = definition(data, year, A, B, def_args)
        if link_type == NEGATIVE_LINK:
            negative_edges_count += 1
        elif link_type == POSITIVE_LINK:
            positive_edges_count += 1
        elif link_type == NO_LINK:
            no_edge_count += 1
    edges_count = positive_edges_count + negative_edges_count
    return edges_count, positive_edges_count, negative_edges_count, no_edge_count


@memoize
def link_type_ratio(data, year, definition, def_args, link_type):
    total, positives, negatives, no_edge_count = sign_distributions(data, year, definition, def_args)
    if link_type == POSITIVE_LINK:
        return positives * 1.0 / total
    if link_type == NEGATIVE_LINK:
        return negatives * 1.0 / total
    if link_type == NO_LINK:
        return no_edge_count * 1.0 / total
    return None


def table1(data, year, definition, def_args):
    def link_exists_def(data, year, A, B, def_args1):
        if 'World' in [A, B]: return 0
        return 0 if definition(data, year, A, B, def_args) == NO_LINK else 1

    edges_count, positives, negatives, _ = sign_distributions(data, year, definition, def_args)
    return {'Name': 'Table1',
            'Nodes': len(data.countries()),
            'Edges': edges_count,
            '+ edges': positives * 100.0 / edges_count,
            '- edges': negatives * 100.0 / edges_count,
            'Traids': number_of_traids(__matrix_cube(get_relationship_matrix(data, year, link_exists_def, {})))
    }


def table2(data, year, definition, def_args):
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
