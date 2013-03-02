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
