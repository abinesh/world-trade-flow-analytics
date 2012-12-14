from project.export_data.strongties import is_there_a_strong_tie_method_B

NEGATIVE_LINK = "negative"
POSITIVE_LINK = "positive"
NO_LINK = "missing"

def args_for_definition_A(lower_bound, upper_bound):
    return {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }


def definition_A(data, year, country_A, country_B, args):
    return POSITIVE_LINK if is_there_a_strong_tie_method_B(data, year, country_A, country_B, args.lower_bound,
        args.upper_bound) else NEGATIVE_LINK


def args_for_definition_B(sliding_window_size):
    return {
        'sliding_window_size': sliding_window_size
    }


def definition_B(data, year, country_A, country_B, args):
    ACCELERATING = "+"
    DECELERATING = "-"
    STEADY_RISING = "s+"
    STEADY_FALLING = "s-"
    CANT_ESTABLISH_TREND = "null"

    def export_growth(data, year, A, B):
        actual_export_percentage = data.export_data_as_percentage(year, A, B, True)
        if actual_export_percentage is None:
            return CANT_ESTABLISH_TREND
        (slope, lower_limit, upper_limit) = data.bollinger_band_range(year - args['sliding_window_size'] - 1, year - 1,
            A, B)

        if lower_limit is None or upper_limit is None:
            return None, CANT_ESTABLISH_TREND
        elif actual_export_percentage < lower_limit:
            return DECELERATING
        elif actual_export_percentage > upper_limit:
            return ACCELERATING
        else:
            return STEADY_RISING if slope > 0 else STEADY_FALLING

    def combine_trends(trend_A, trend_B):
        if CANT_ESTABLISH_TREND in [trend_A, trend_B]:
            return NO_LINK
        elif trend_A in [ACCELERATING, STEADY_RISING] and trend_B in [ACCELERATING, STEADY_RISING]:
            return POSITIVE_LINK
        else:
            return NEGATIVE_LINK

    trend_A = export_growth(data, year, country_A, country_B)
    trend_B = export_growth(data, year, country_B, country_A)
    return combine_trends(trend_A, trend_B)


