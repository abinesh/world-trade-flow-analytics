from itertools import combinations
from project.signed_networks.definitions import NO_LINK
from project.util import memoize


@memoize
def new_and_total_links(data, definition, def_args, year, look_back_duration):
    new = 0
    total = 0
    for (A, B) in combinations(data.all_countries, 2):
        if definition(data, year, A, B, def_args) != NO_LINK:
            total += 1
            new += 1 if definition(data, year - look_back_duration, A, B, def_args) == NO_LINK else 0
    return new, total


def percentage_of_new_links(data, definition, def_args, year, look_back_duration):
    (new, total) = new_and_total_links(data, definition, def_args, year, look_back_duration)
    return new * 1.0 / total
