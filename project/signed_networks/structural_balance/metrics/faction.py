from math import sqrt, ceil
import sys
from project.countries import world_excluded_countries_list
from project.signed_networks.definitions import POSITIVE_LINK, NO_LINK
from project.signed_networks.structural_balance.metrics.vertex import positive_edge_count, negative_edge_count
from project.util import memoize

DEFAULT_COUNTRIES_LIST = world_excluded_countries_list()


def _add_to_slope_map(slope_map, key, new_list_item):
    if key not in slope_map: slope_map[key] = []
    prev_entry = slope_map[key]
    prev_entry.append(new_list_item)


def _compute_slope(p1, p2):
    if p1[0] - p2[0] == 0: return sys.float_info.max
    return (p1[1] - p2[1]) / (p1[0] - p2[0])


def _distance_from_origin(point):
    return sqrt(point[0] * point[0] + point[1] * point[1])


def detect_factions_from_co_movements(positives_and_negatives, window_size, year):
    countries_list = positives_and_negatives[year].keys()
    movements_per_country = {}
    for current_year in range(year - window_size + 1, year + 1):
        previous_year = current_year - 1
        for C in countries_list:
            current_year_position = positives_and_negatives[current_year][C]
            previous_year_position = positives_and_negatives[previous_year][C]
            slope = ceil(_compute_slope(current_year_position, previous_year_position))
            distance_diff_from_origin = _distance_from_origin(current_year_position) - \
                                        _distance_from_origin(previous_year_position)

            _add_to_slope_map(movements_per_country, C,
                              "(%.3f,%s)" % (slope, '+' if distance_diff_from_origin > 0 else '-'))
    countries_that_co_moved = {}
    for key in movements_per_country:
        _add_to_slope_map(countries_that_co_moved, str(movements_per_country[key]), key)
    return countries_that_co_moved.values()


@memoize
def positives_and_negatives_matrix(data, definition, def_args, years, countries=DEFAULT_COUNTRIES_LIST):
    def flatten(multilist): return [item for sublist in multilist for item in sublist]

    def country_row(C):
        def delta_from_mean(C, years, year, edge_type):
            mean = sum([edge_type(data, Y, C, definition, def_args) for Y in years]) * 1.0 / len(years)
            return edge_type(data, year, C, definition, def_args) - mean

        return flatten([[delta_from_mean(C, years, year, positive_edge_count),
                         delta_from_mean(C, years, year, negative_edge_count)] for year in years])

    return [country_row(C) for C in countries]


@memoize
def adjacency_matrix_row(data, definition, def_args, year, A, countries=DEFAULT_COUNTRIES_LIST):
    return [0 if A == B or definition(data, year, A, B, def_args) == NO_LINK
            else 1 if definition(data, year, A, B, def_args) == POSITIVE_LINK
    else -1 for B in countries]


@memoize
def adjacency_matrix(data, definition, def_args, year, countries=DEFAULT_COUNTRIES_LIST):
    return [adjacency_matrix_row(data, definition, def_args, year, A, countries) for A in countries]


def matrix_py_to_matlab(matrix, only_first_row=False):
    mat_as_matlab = [(' '.join([str(value) for value in row])) for row in matrix]
    return ';'.join(mat_as_matlab) if not only_first_row else mat_as_matlab[0]


def adjacency_matrix_matlab(data, definition, def_args, year, countries=DEFAULT_COUNTRIES_LIST):
    return matrix_py_to_matlab(adjacency_matrix(data, definition, def_args, year, countries))


def positives_and_negatives_matrix_matlab(data, definition, def_args, years, countries=DEFAULT_COUNTRIES_LIST):
    return matrix_py_to_matlab(positives_and_negatives_matrix(data, definition, def_args, years, countries))


def corrcoef_py_to_matlab(var_name, matrix, only_first_row=False):
    return "%s=[%s]" % (var_name, matrix_py_to_matlab(matrix, only_first_row))


def concat_countries(countries, years):
    row = []
    for year in years:
        row += ['%s-%d' % (c, year) for c in countries]
    return row