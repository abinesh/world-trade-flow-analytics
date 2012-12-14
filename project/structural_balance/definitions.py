from project.export_data.strongties import is_there_a_strong_tie_method_B

NEGATIVE_LINK = "negative"
POSITIVE_LINK = "positive"
NO_LINK = "null"

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
    DECELERATING = "decelerating"
    ACCELERATING = "accelerating"
    STABLE_TREND = "stable"
    CANT_ESTABLISH_TREND = "null"

    def export_growth(data, year, A, B):
        actual_export = data.export_data(year, A, B)
        if actual_export is None:
            return CANT_ESTABLISH_TREND
        (lower_limit, upper_limit) = data.expected_export_range(year - args['sliding_window_size'] - 1, year - 1, A, B)

        if lower_limit is None or upper_limit is None:
            return CANT_ESTABLISH_TREND
        elif actual_export < lower_limit:
            return DECELERATING
        elif lower_limit <= actual_export <= upper_limit:
            return STABLE_TREND
        else:
            return ACCELERATING

    def combine_trends(A, B):
        if A == CANT_ESTABLISH_TREND or B == CANT_ESTABLISH_TREND:
            return NO_LINK
        elif A == DECELERATING or B == DECELERATING:
            return NEGATIVE_LINK
        else:
            return POSITIVE_LINK

    A_export_to_B = export_growth(data, year, country_A, country_B)
    B_export_to_A = export_growth(data, year, country_B, country_A)
    return combine_trends(A_export_to_B, B_export_to_A)


