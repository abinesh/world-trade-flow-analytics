from project.signed_networks.definitions import POSITIVE_LINK, NO_LINK

max_common_neighbours_possible = 201

def compute_fraction(map):
    result = []
    for i in range(0, max_common_neighbours_possible + 1):
        fraction = 0
        if i in map:
            list = map[i]
            fraction = list.count(POSITIVE_LINK) * 1.0 / (len(list) - list.count(NO_LINK))
        result.append(fraction)
    return result
