from math import sqrt, ceil
import sys
from project.countries import world_excluded_countries_list
from project.signed_networks.definitions import POSITIVE_LINK, NO_LINK
from project.signed_networks.structural_balance.metrics.vertex import positive_edge_count, negative_edge_count
from project.util import memoize, std_dev

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
def positives_and_negatives_matrix(data, definition, def_args, years, countries=DEFAULT_COUNTRIES_LIST,
                                   normalize_row_or_column='column'):
    def flatten(multilist):
        return [item for sublist in multilist for item in sublist]

    def normalize(data_point, data_points):
        very_small_value = 0.000001
        mean = sum(data_points) * 1.0 / len(data_points)
        stddev = std_dev(data_points)
        if stddev == 0:
            stddev = very_small_value if mean == 0 else mean * very_small_value
        return (data_point - mean) / (3.0 * stddev)

    def country_row_with_row_normalisation(C):
        def delta_from_mean_by_thrice_std_dev(C, years, year, edge_type):
            data_point = edge_type(data, year, C, definition, def_args)
            data_points = [edge_type(data, Y, C, definition, def_args) for Y in years]
            return normalize(data_point, data_points)

        return flatten([[delta_from_mean_by_thrice_std_dev(C, years, year, positive_edge_count),
                         delta_from_mean_by_thrice_std_dev(C, years, year, negative_edge_count)] for year in years])

    def country_row_with_column_normalisation(C, countries):
        def all_countries_degree_list(countries, year, degree_function):
            return [degree_function(data, year, C, definition, def_args) for C in countries]

        return flatten([[normalize(positive_edge_count(data, year, C, definition, def_args),
                                   all_countries_degree_list(countries, year, positive_edge_count)),
                         normalize(negative_edge_count(data, year, C, definition, def_args),
                                   all_countries_degree_list(countries, year, negative_edge_count))] for year in years])

    if normalize_row_or_column == 'row':
        return [country_row_with_row_normalisation(C) for C in countries]
    elif normalize_row_or_column == 'column':
        return [country_row_with_column_normalisation(C, countries) for C in countries]
    else:
        assert False


@memoize
def adjacency_matrix_row(data, definition, def_args, year, A, countries=DEFAULT_COUNTRIES_LIST):
    return [0 if A == B or definition(data, year, A, B, def_args) == NO_LINK
            else 1 if definition(data, year, A, B, def_args) == POSITIVE_LINK
    else -1 for B in countries]


@memoize
def adjacency_matrix(data, definition, def_args, year, countries=DEFAULT_COUNTRIES_LIST):
    return [adjacency_matrix_row(data, definition, def_args, year, A, countries) for A in countries]


def matrix_py_to_matlab(matrix, only_first_row=False):
    mat_as_matlab = [(' '.join(['%.5g' % value for value in row])) for row in matrix]
    return ';'.join(mat_as_matlab) if not only_first_row else mat_as_matlab[0]


def adjacency_matrix_matlab(data, definition, def_args, year, countries=DEFAULT_COUNTRIES_LIST):
    return matrix_py_to_matlab(adjacency_matrix(data, definition, def_args, year, countries))


def positives_and_negatives_matrix_matlab(data, definition, def_args, years, countries=DEFAULT_COUNTRIES_LIST,
                                          normalize_row_or_column='column'):
    return matrix_py_to_matlab(positives_and_negatives_matrix(data, definition, def_args, years, countries, normalize_row_or_column))


def corrcoef_py_to_matlab(var_name, matrix, only_first_row=False):
    return "%s=[%s]" % (var_name, matrix_py_to_matlab(matrix, only_first_row))


def concat_countries(countries, years):
    row = []
    for year in years:
        row += ['%s-%d' % (c, year) for c in countries]
    return row
