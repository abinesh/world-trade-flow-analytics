from itertools import combinations
from project.signed_networks.definitions import NO_LINK
from project.util import memoize


def is_new_edge(data, def_args, definition, year, A, B, look_back_duration):
    return definition(data, year - look_back_duration, A, B, def_args) == NO_LINK


@memoize
def new_and_total_edges(data, definition, def_args, year, look_back_duration):
    new = 0
    total = 0
    for (A, B) in combinations(data.all_countries, 2):
        if definition(data, year, A, B, def_args) != NO_LINK:
            total += 1
            new += 1 if is_new_edge(data, def_args, definition, year, A, B, look_back_duration) else 0
    return new, total


@memoize
def edge_sign_change_and_total_edges(data, definition, def_args, year, look_back_duration):
    sign_change_count = 0
    total = 0
    for (A, B) in combinations(data.all_countries, 2):
        if definition(data, year, A, B, def_args) != NO_LINK:
            current_sign = definition(data, year, A, B, def_args)
            previous_sign = definition(data, year - look_back_duration, A, B, def_args)
            if current_sign != NO_LINK and previous_sign != NO_LINK:
                total += 1
                sign_change_count += 1 if current_sign != previous_sign else 0
    return sign_change_count, total


def percentage_of_new_edges_over_time(data, definition, def_args, year, look_back_duration):
    (new, total) = new_and_total_edges(data, definition, def_args, year, look_back_duration)
    return new * 1.0 / total


def percentage_of_edge_sign_changes_over_time(data, definition, def_args, year, look_back_duration):
    (new, total) = edge_sign_change_and_total_edges(data, definition, def_args, year, look_back_duration)
    return new * 1.0 / total


def hops_count_before_edge_vs_count(data, definition, def_args, year, look_back_duration):
    return [(1, 10), (2, 15)]

