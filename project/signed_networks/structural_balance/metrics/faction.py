from math import sqrt, ceil
import sys


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
