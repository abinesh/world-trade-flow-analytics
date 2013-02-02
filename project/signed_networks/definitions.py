from project.export_data.strongties import is_there_a_strong_tie_method_B, strong_tie_def_args
from project.traids_vs_degree_plot import config
from project.util import file_safe, memoize

NEGATIVE_LINK = "negative"
POSITIVE_LINK = "positive"
NO_LINK = "missing"

def args_for_definition_A(lower_bound, upper_bound):
    return {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }


@memoize
def definition_A(data, year, country_A, country_B, args):
    return POSITIVE_LINK if is_there_a_strong_tie_method_B(data, year, country_A, country_B, args) else NEGATIVE_LINK


def args_for_definition_B(sliding_window_size, trend_combinations_log=None):
    return {
        'sliding_window_size': sliding_window_size,
        'trend_combinations_log': trend_combinations_log
    }


@memoize
def definition_B(data, year, country_A, country_B, args):
    ACCELERATING = "+"
    DECELERATING = "-"
    STEADY_RISING = "s+"
    STEADY_FALLING = "s-"
    CANT_ESTABLISH_TREND = "null"

    def export_growth(data, year, A, B):
        if not is_there_a_strong_tie_method_B(data, year, A, B,
            strong_tie_def_args(config.STRONG_TIES_LOWER_BOUND, config.STRONG_TIES_UPPER_BOUND)):
            return CANT_ESTABLISH_TREND
        actual_export_percentage = data.export_data_as_percentage(year, A, B, True)
        if actual_export_percentage is None:
            return CANT_ESTABLISH_TREND
        (slope, lower_limit, upper_limit) = data.bollinger_band_range(year - args['sliding_window_size'] - 1, year - 1,
            A, B)

        if lower_limit is None or upper_limit is None:
            return CANT_ESTABLISH_TREND
        elif actual_export_percentage < lower_limit:
            return DECELERATING
        elif actual_export_percentage > upper_limit:
            return ACCELERATING
        else:
            return STEADY_RISING if slope > 0 else STEADY_FALLING

    def combine_trends(trend_A, trend_B):
        if CANT_ESTABLISH_TREND in [trend_A, trend_B]:
            if  args['trend_combinations_log'] is not None: args['trend_combinations_log'].write(
                "%s,%s,%s\n" % (trend_A, trend_B, NO_LINK))
            return NO_LINK
        elif trend_A in [ACCELERATING, STEADY_RISING] and trend_B in [ACCELERATING, STEADY_RISING]:
            if args['trend_combinations_log'] is not None: args['trend_combinations_log'].write(
                "%s,%s,%s\n" % (trend_A, trend_B, POSITIVE_LINK))
            return POSITIVE_LINK
        else:
            if args['trend_combinations_log'] is not None: args['trend_combinations_log'].write(
                "%s,%s,%s\n" % (trend_A, trend_B, NEGATIVE_LINK))
            return NEGATIVE_LINK

    trend_A = export_growth(data, year, country_A, country_B)
    trend_B = export_growth(data, year, country_B, country_A)
    return combine_trends(trend_A, trend_B)


def __combine_links(one_way, other_way):
    if NO_LINK in [one_way, other_way]: return NO_LINK
    if NEGATIVE_LINK in [one_way, other_way]: return NEGATIVE_LINK
    return POSITIVE_LINK


def args_for_definition_C(min_export_quantity_threshold, export_percentage_cutoff_threshold, f=None):
    return {
        'min_export_quantity_threshold': min_export_quantity_threshold,
        'export_percentage_cutoff_threshold': export_percentage_cutoff_threshold,
        'f': f
    }


def __log_to_file(T2, args, country_A, country_B, one_way, other_way, year):
    if args['f'] is not None:
        args['f'].write(
            "%d,%s,%s,%d,%s,%s\n" % (year, file_safe(country_A), file_safe(country_B), T2, one_way, other_way))


def __def_C__(args, country_A, country_B, data, year, t1_function):
    def __def_C_directed_link(data, year, A, B, T1, T2, t1_function):
        if t1_function(A, B) < T1: return NO_LINK
        if data.export_data(year, A, B, return_this_for_missing_datapoint=-1) == -1: return NO_LINK
        if data.export_data(year, A, B) is None or data.export_data(year, A, B) == 0:
            if year > data.first_trade_year(A, B):
                return NEGATIVE_LINK
            else:
                return NO_LINK
        if data.export_data_as_percentage(year, A, B) * 100 >= T2: return POSITIVE_LINK
        return NEGATIVE_LINK

    T1 = args['min_export_quantity_threshold']
    T2 = args['export_percentage_cutoff_threshold']

    one_way = __def_C_directed_link(data, year, country_A, country_B, T1, T2, t1_function)
    other_way = __def_C_directed_link(data, year, country_B, country_A, T1, T2, t1_function)

    __log_to_file(T1, args, country_A, country_B, one_way, other_way, year)
    return __combine_links(one_way, other_way)


@memoize
def definition_C1(data, year, country_A, country_B, args):
    return __def_C__(args, country_A, country_B, data, year, data.total_exports_from_C1_to_C2)


@memoize
def definition_C2(data, year, country_A, country_B, args):
    return __def_C__(args, country_A, country_B, data, year, data.total_non_nan_points_from_C1_to_C2)


def args_for_definition_D(threshold, f=None):
    return {
        'threshold': threshold,
        'f': f
    }


@memoize
def _def_D_first_positive(data, A, B, T):
    for year in data.all_years:
        if B in data.top_T_percent_exports(A, year, T):
            return year
    return 9999


@memoize
def definition_D(data, year, country_A, country_B, args):
    def _def_D_directed_link(T, A, B, data, year):
        if data.export_data(year, A, B, -1) == -1: return NO_LINK
        if B in data.top_T_percent_exports(A, year, T): return POSITIVE_LINK
        if _def_D_first_positive(data, A, B, T) > year: return NO_LINK
        return NEGATIVE_LINK

    T = args['threshold']

    one_way = _def_D_directed_link(T, country_A, country_B, data, year)
    other_way = _def_D_directed_link(T, country_B, country_A, data, year)

    __log_to_file(T, args, country_A, country_B, one_way, other_way, year)
    return __combine_links(one_way, other_way)


