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


