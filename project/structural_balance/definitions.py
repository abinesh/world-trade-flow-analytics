from project.export_data.strongties import is_there_a_strong_tie_method_B

NEGATIVE_LINK = "negative"
POSITIVE_LINK = "positive"
NO_LINK = "null"

def args_for_definition_A(lower_bound, upper_bound):
    return {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }


def args_for_definition_B():
    return {}


def definition_A(data, year, country_A, country_B, args):
    return POSITIVE_LINK if is_there_a_strong_tie_method_B(data, year, country_A, country_B, args.lower_bound,
        args.upper_bound) else NEGATIVE_LINK


def definition_B(data, year, country_A, country_B, args):
    return POSITIVE_LINK


