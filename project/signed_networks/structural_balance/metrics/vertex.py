from project.signed_networks.definitions import POSITIVE_LINK, NEGATIVE_LINK, NO_LINK

def degree_sum(data, year, A, definition, def_args):
    sum = 0
    for B in data.countries():
        if A == B: continue
        link_sign = definition(data, year, A, B, def_args)
        sum += 1 if link_sign == POSITIVE_LINK else -1 if link_sign == NEGATIVE_LINK else 0
    return sum


def degree_count(data, year, A, definition, def_args):
    return len([1 for B in data.countries() if A != B and definition(data, year, A, B, def_args) != NO_LINK])

