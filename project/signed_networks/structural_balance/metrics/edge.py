from itertools import combinations
from project.signed_networks.definitions import POSITIVE_LINK, NO_LINK

max_common_neighbours_possible = 201

def compute_fraction(map):
    result = []
    for i in range(0, max_common_neighbours_possible + 1):
        fraction = 0
        if i in map:
            (negative_edges, positive_edges) = map[i]
            fraction = positive_edges * 1.0 / (positive_edges + negative_edges)
        result.append(fraction)
    return result


def common_neighbours_count(data, year, A, B, definition, def_args):
    common_neighbour_count = 0
    for C in data.countries():
        if C == A or C == B: continue
        if NO_LINK not in [definition(data, year, A, C, def_args), definition(data, year, B, C, def_args)]:
            common_neighbour_count += 1
    return common_neighbour_count


def compute_map(data, year, definition, def_args):
    result = {}
    for A, B in combinations(data.countries(), 2):
        link_sign = definition(data, year, A, B, def_args)
        if link_sign == NO_LINK: continue
        common_neighbour_count = common_neighbours_count(data, year, A, B, definition, def_args)
        if common_neighbour_count not in result:
            result[common_neighbour_count] = (0, 0)
        (negative_edges, positive_edges) = result[common_neighbour_count]
        result[common_neighbour_count] = (negative_edges, positive_edges + 1) if link_sign == POSITIVE_LINK\
        else (negative_edges + 1, positive_edges)
    return result


