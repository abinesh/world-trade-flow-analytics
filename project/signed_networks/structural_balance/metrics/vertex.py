from project.signed_networks.definitions import POSITIVE_LINK, NEGATIVE_LINK, NO_LINK
from project.util import memoize


@memoize
def degree_sum(data, year, A, definition, def_args):
    sum = 0
    for B in data.countries():
        if A == B: continue
        link_sign = definition(data, year, A, B, def_args)
        sum += 1 if link_sign == POSITIVE_LINK else -1 if link_sign == NEGATIVE_LINK else 0
    return sum


def degree_count(data, year, A, definition, def_args):
    return positive_edge_count(data, year, A, definition, def_args) \
           + negative_edge_count(data, year, A, definition, def_args)


@memoize
def edge_count(A, data, def_args, definition, year, edge_type):
    return len([1 for B in data.countries() if A != B and definition(data, year, A, B, def_args) == edge_type])


def positive_edge_count(data, year, A, definition, def_args):
    return edge_count(A, data, def_args, definition, year, POSITIVE_LINK)


def negative_edge_count(data, year, A, definition, def_args):
    return edge_count(A, data, def_args, definition, year, NEGATIVE_LINK)

