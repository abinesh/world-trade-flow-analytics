from project.export_data.strongties import is_there_a_strong_tie_method_B, strong_tie_def_args
from project.traids_vs_degree_plot import config

NEGATIVE_LINK = "negative"
POSITIVE_LINK = "positive"
NO_LINK = "missing"

def args_for_definition_A(lower_bound, upper_bound):
    return {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }


def definition_A(data, year, country_A, country_B, args):
    return POSITIVE_LINK if is_there_a_strong_tie_method_B(data, year, country_A, country_B, args) else NEGATIVE_LINK


def args_for_definition_B(sliding_window_size, trend_combinations_log=None):
    return {
        'sliding_window_size': sliding_window_size,
        'trend_combinations_log': trend_combinations_log
    }


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


def args_for_definition_D(threshold):
    return {
        'threshold': threshold,
    }


def definition_D(data, year, country_A, country_B, args):
    T = args['threshold']

    def is_C2_in_top_T_percentage_exports_of_C1(C1, C2):
        (total, previous_percentage, current_percentage) = (0, -1, -1)
        for (C, percentage) in data.sorted_list_of_export_percentages(C1, year):
            total += percentage
            if C == C2: return True
            if total > T: return False
        return False

    one_way = NO_LINK\
    if data.export_data(year, country_A, country_B) == 0\
    else POSITIVE_LINK if is_C2_in_top_T_percentage_exports_of_C1(country_A, country_B)\
    else NEGATIVE_LINK

    other_way = NO_LINK\
    if data.export_data(year, country_B, country_A) == 0\
    else POSITIVE_LINK if is_C2_in_top_T_percentage_exports_of_C1(country_B, country_A)\
    else NEGATIVE_LINK

    if NO_LINK in [one_way, other_way]: return NO_LINK
    if NEGATIVE_LINK in [one_way, other_way]: return NEGATIVE_LINK
    return POSITIVE_LINK


