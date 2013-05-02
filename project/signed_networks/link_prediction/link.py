from itertools import combinations
import numpy
import scipy
from project.countries import index_of_country
from project.signed_networks.definitions import NO_LINK
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
def count_hops(data, definition, def_args, year, A, B):
    scipy_matrix = scipy.asmatrix(scipy.array(unsigned_adjacency_matrix(data, definition, def_args, year)))
    multiplied_matrix = scipy.asmatrix(scipy.array(unsigned_adjacency_matrix(data, definition, def_args, year)))
    hop_count = 1
    while hop_count < len(data.countries()):
        if multiplied_matrix.tolist()[index_of_country(A)][index_of_country(B)] != 0:
            return hop_count
        multiplied_matrix = numpy.dot(multiplied_matrix, scipy_matrix)
        hop_count += 1
    return INFINITE_HOPS


@memoize
def hops_count_before_edge_vs_count(data, definition, def_args, year, look_back_duration):
    counts = Counts()
    infinity_count = 0
    for (A, B) in combinations(data.countries(), 2):
        if is_new_edge(data, def_args, definition, year, A, B, look_back_duration):
            count = count_hops(data, definition, def_args, year - look_back_duration, A, B)
            if count == INFINITE_HOPS: infinity_count += 1
            counts.record(count)
    return_val = counts.as_tuples_list()
    last_value= return_val[-1:][0][0]
    return_val.append((last_value+5, infinity_count))
    return return_val

