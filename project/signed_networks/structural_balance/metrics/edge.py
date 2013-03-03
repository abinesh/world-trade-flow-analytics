from itertools import combinations
from project.signed_networks.definitions import POSITIVE_LINK, NO_LINK

max_common_neighbours_possible = 201

def compute_fraction_of_positive_edges(map):
    result = []
    for i in range(0, max_common_neighbours_possible + 1):
        fraction = 0
        if i in map:
            (negative_edges, positive_edges) = map[i]
            fraction = positive_edges * 1.0 / (positive_edges + negative_edges)
        result.append(fraction)
    return result


def common_neighbours(data, year, A, B, definition, def_args):
    return [C for C in data.countries() if C not in [A, B]
    and NO_LINK not in [definition(data, year, A, C, def_args), definition(data, year, B, C, def_args)]]


def compute_map(data, year, definition, def_args):
    result = {}
    for A, B in combinations(data.countries(), 2):
        link_sign = definition(data, year, A, B, def_args)
        if link_sign == NO_LINK: continue
        common_neighbour_count = len(common_neighbours(data, year, A, B, definition, def_args))
        if common_neighbour_count not in result:
            result[common_neighbour_count] = (0, 0)
        (negative_edges, positive_edges) = result[common_neighbour_count]
        result[common_neighbour_count] = (negative_edges, positive_edges + 1) if link_sign == POSITIVE_LINK\
        else (negative_edges + 1, positive_edges)
    return result


def fraction_of_embedded_positive_signs(data, year, definition, def_args):
    return compute_fraction_of_positive_edges(compute_map(data, year, definition, def_args))


def traid_type(data, year, A, B, C, definition, def_args):
    side1 = definition(data, year, A, B, def_args)
    side2 = definition(data, year, B, C, def_args)
    side3 = definition(data, year, C, A, def_args)
    traid = [side1, side2, side3]
    assert NO_LINK not in traid
    return "T%d" % (traid.count(POSITIVE_LINK))

# Todo: number of balanced triangles vs number of common neighbours
def traids_per_common_edge_count(data, year, definition, def_args):
    def to_list(map):
        return [map[i] if i in map else (0, 0, 0, 0)
                for i in range(0, max_common_neighbours_possible + 1)]

    result = {}
    for A, B in combinations(data.countries(), 2):
        side1 = definition(data, year, A, B, def_args)
        if side1 != NO_LINK:
            neighbours = common_neighbours(data, year, A, B, definition, def_args)
            if len(neighbours) not in result: result[len(neighbours)] = (0, 0, 0, 0)
            for C in neighbours:
                (old_t0, old_t1, old_t2, old_t3) = result[len(neighbours)]
                t = traid_type(data, year, A, B, C, definition, def_args)
                if t == "T0": result[len(neighbours)] = (old_t0 + 1, old_t1, old_t2, old_t3)
                if t == "T1": result[len(neighbours)] = (old_t0, old_t1 + 1, old_t2, old_t3)
                if t == "T2": result[len(neighbours)] = (old_t0, old_t1, old_t2 + 1, old_t3)
                if t == "T3": result[len(neighbours)] = (old_t0, old_t1, old_t2, old_t3 + 1)
    return to_list(result)
