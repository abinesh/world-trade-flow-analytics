from itertools import combinations
from project.signed_networks.definitions import POSITIVE_LINK, NEGATIVE_LINK, NO_LINK


def triad_type(data, year, A, B, C, definition, def_args):
    linkAtoB = definition(data, year, A, B, def_args)
    linkBtoC = definition(data, year, B, C, def_args)
    linkCtoA = definition(data, year, C, A, def_args)
    triangle = [linkAtoB, linkBtoC, linkCtoA]
    pcount = triangle.count(POSITIVE_LINK)
    ncount = triangle.count(NEGATIVE_LINK)
    mcount = triangle.count(NO_LINK)
    return "T%d%d%d" % ( pcount, ncount, mcount)


def is_traid(data, year, A, B, C, definition, def_args):
    return triad_type(data, year, A, B, C, definition, def_args)[-1:] == '0'


def get_traids(data, year, definition, def_args, traid_type):
    return [(A, B, C) for (A, B, C) in combinations(data.countries(), 3) if
            is_traid(data, year, A, B, C, definition, def_args) and
            triad_type(data, year, A, B, C, definition, def_args)[:2] == traid_type]



