from itertools import combinations
import numpy
import scipy
from project.countries import index_of_country
from project.signed_networks.definitions import NO_LINK, POSITIVE_LINK, NEGATIVE_LINK
from project.signed_networks.structural_balance.metrics.faction import adjacency_matrix, unsigned_adjacency_matrix
from project.util import memoize, Counts

INFINITE_HOPS = 500


def is_new_edge(data, def_args, definition, year, A, B, look_back_duration):
    return definition(data, year - look_back_duration, A, B, def_args) == NO_LINK and \
           definition(data, year, A, B, def_args) != NO_LINK


@memoize
def new_and_total_edges(data, definition, def_args, year, look_back_duration):
    new = 0
    total = 0
    for (A, B) in combinations(data.countries(), 2):
        if definition(data, year, A, B, def_args) != NO_LINK:
            total += 1
            new += 1 if is_new_edge(data, def_args, definition, year, A, B, look_back_duration) else 0
    return new, total


@memoize
def edge_sign_change_and_total_edges(data, definition, def_args, year, look_back_duration):
    sign_change_count = 0
    total = 0
    for (A, B) in combinations(data.countries(), 2):
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


@memoize
def memoize_matrix_mult(A, B):
    return numpy.dot(A, B)


@memoize
def count_hops(data, definition, def_args, year, A, B):
    scipy_matrix = scipy.asmatrix(scipy.array(unsigned_adjacency_matrix(data, definition, def_args, year)))
    multiplied_matrix = scipy.asmatrix(scipy.array(unsigned_adjacency_matrix(data, definition, def_args, year)))
    hop_count = 1
    while hop_count < len(data.countries()):
        if multiplied_matrix.tolist()[index_of_country(A)][index_of_country(B)] != 0:
            return hop_count
        multiplied_matrix = memoize_matrix_mult(multiplied_matrix, scipy_matrix)
        hop_count += 1
    return INFINITE_HOPS


def inf_scale_adjust(hops):
    inf_x_axis_value = max([hop[0][-1][0] for hop in hops]) + 1
    updated_hops = []
    for hops_index in range(0, len(hops)):
        updated_hop = hops[hops_index][0]
        for index in range(len(updated_hop) + 1, inf_x_axis_value):
            updated_hop.append((index, 0))
        updated_hop.append((inf_x_axis_value, hops[hops_index][1]))
        updated_hops.append(updated_hop)
    return updated_hops, inf_x_axis_value


@memoize
def hops_count_before_edge_vs_count(data, definition, def_args, year, look_back_duration):
    counts = Counts()
    infinity_count = 0
    for (A, B) in combinations(data.countries(), 2):
        if is_new_edge(data, def_args, definition, year, A, B, look_back_duration):
            count = count_hops(data, definition, def_args, year - look_back_duration, A, B)
            if count == INFINITE_HOPS:
                infinity_count += 1
            else:
                counts.record(count)
    return counts.as_tuples_list(), infinity_count


@memoize
def count_of_bridge_configs_between(data, definition, def_args, year, A, B):
    (twoPlus, plusMinus, twoMinus) = 0, 0, 0
    for C in data.countries():
        if C not in [A, B]:
            cToA = definition(data, year, C, A, def_args)
            cToB = definition(data, year, C, B, def_args)
            both_links = [cToA, cToB]
            if NO_LINK not in both_links:
                if both_links.count(POSITIVE_LINK) == 2: twoPlus += 1
                if both_links.count(NEGATIVE_LINK) == 2: twoMinus += 1
                if both_links.count(POSITIVE_LINK) == 1 and both_links.count(NEGATIVE_LINK) == 1: plusMinus += 1
    return (twoPlus, plusMinus, twoMinus)


@memoize
def _memoize_count_of_bridge_configs(data, def_args, definition, look_back_duration, year):
    counts = {'2+': 0, '+-': 0, '2-': 0}
    for (A, B) in combinations(data.countries(), 2):
        if is_new_edge(data, def_args, definition, year, A, B, look_back_duration):
            (twoPlus, plusMinus, twoMinus) = count_of_bridge_configs_between(data, definition, def_args,
                                                                             year - look_back_duration, A, B)
            counts['2+'] += twoPlus
            counts['+-'] += plusMinus
            counts['2-'] += twoMinus
    return counts


def count_of_bridge_configs(data, definition, def_args, year, look_back_duration, config):
    counts = _memoize_count_of_bridge_configs(data, def_args, definition, look_back_duration, year)
    return counts[config]

