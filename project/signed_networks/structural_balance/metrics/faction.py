from math import sqrt, ceil
import sys
from project.signed_networks.definitions import POSITIVE_LINK, NEGATIVE_LINK, NO_LINK
from project.signed_networks.structural_balance.metrics.vertex import positive_edge_count, negative_edge_count
from project.util import memoize


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
def positives_and_negatives_matrix(data, definition, def_args, years, countries=None):
    if countries is None: countries = data.countries()

    def flatten(multilist): return [item for sublist in multilist for item in sublist]

    def country_row(C):
        def delta_from_mean(C, years, year, edge_type):
            mean = sum([edge_type(data, Y, C, definition, def_args) for Y in years]) * 1.0 / len(years)
            return edge_type(data, year, C, definition, def_args) - mean

        return flatten([[delta_from_mean(C, years, year, positive_edge_count),
                         delta_from_mean(C, years, year, negative_edge_count)] for year in years])

    return [country_row(C) for C in countries]

@memoize
def adjacency_matrix(data, definition, def_args, year, countries=None):
    if countries is None: countries = data.countries()

    def country_row(A):
        return [0 if A == B or definition(data, year, A, B, def_args) == NO_LINK
                else 1 if definition(data, year, A, B, def_args) == POSITIVE_LINK
        else -1 for B in countries]

    return [country_row(A) for A in countries]


def adjacency_matrix_matlab(data, definition, def_args, year, countries=None):
    return str(adjacency_matrix(data, definition, def_args, year, countries)) \
        .replace("], [", ";") \
        .replace("[", "") \
        .replace("]", "") \
        .replace(",", "")


def positives_and_negatives_matrix_matlab(data, definition, def_args, years, countries=None):
    return str(positives_and_negatives_matrix(data, definition, def_args, years, countries)) \
        .replace("], [", ";") \
        .replace("[", "") \
        .replace("]", "") \
        .replace(",", "")


