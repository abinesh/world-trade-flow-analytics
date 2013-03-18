from math import sqrt


def _add_to_slope_map(slope_map, key, C):
    if key not in slope_map: slope_map[key] = []
    prev_entry = slope_map[key]
    prev_entry.append(C)


def _compute_slope(p1, p2):
    return (p1[1] - p2[1]) / (p1[0] - p2[0])


def _distance_from_origin(point):
    return sqrt(point[0] * point[0] + point[1] * point[1])


def detect_factions_from_co_movements(positives_and_negatives, window_size, year):
    countries_list = positives_and_negatives[year].keys()
    slope_map = {}
    for current_year in range(year - window_size + 1, year + 1):
        previous_year = current_year - 1
        for C in countries_list:
            current_year_position = positives_and_negatives[current_year][C]
            previous_year_position = positives_and_negatives[previous_year][C]
            slope = _compute_slope(current_year_position, previous_year_position)
            distance_diff_from_origin = _distance_from_origin(current_year_position) - \
                                        _distance_from_origin(previous_year_position)

            _add_to_slope_map(slope_map, "(%.3f,%s)" % (slope, '+' if distance_diff_from_origin > 0 else '-'), C)
    return slope_map.values()
