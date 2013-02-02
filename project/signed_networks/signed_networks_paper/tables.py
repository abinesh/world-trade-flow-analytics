#Implementation of tables listed in paper http://www.cs.cornell.edu/home/kleinber/chi10-signed.pdf
from itertools import combinations
from project import countries
from project.export_data.strongties import number_of_traids, __matrix_cube, get_relationship_matrix
from project.signed_networks.definitions import NO_LINK, NEGATIVE_LINK, POSITIVE_LINK

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
    return {'Nodes': len(data.countries()),
            'Edges': edges_count,
            '+ edges': positive_edges_count * 100.0 / edges_count,
            '- edges': negative_edges_count * 100.0 / edges_count,
            'Traids': number_of_traids(__matrix_cube(get_relationship_matrix(data, year, link_exists_def, {})))
    }


def table2(data, year, definition, def_args):
    t0, t1, t2, t3 = 0, 0, 0, 0
    for (A, B, C) in combinations(data.countries(), 3):
        side1 = definition(data, year, A, B, def_args)
        side2 = definition(data, year, B, C, def_args)
        side3 = definition(data, year, C, A, def_args)
        if side1 == NO_LINK or side2 == NO_LINK or side3 == NO_LINK: continue
        positive_sides = 0
        for side in [side1, side2, side3]:
            if side == POSITIVE_LINK: positive_sides += 1
        if positive_sides == 0: t0 += 1
        if positive_sides == 1: t1 += 1
        if positive_sides == 2: t2 += 1
        if positive_sides == 3: t3 += 1
    total = t0 + t1 + t2 + t3
    return {'T0': {'|Ti|': t0, 'p(Ti)': t0 * 1.0 / total},
            'T1': {'|Ti|': t1, 'p(Ti)': t1 * 1.0 / total},
            'T2': {'|Ti|': t2, 'p(Ti)': t2 * 1.0 / total},
            'T3': {'|Ti|': t3, 'p(Ti)': t3 * 1.0 / total}}
