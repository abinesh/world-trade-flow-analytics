from itertools import combinations
from random import uniform
from project.signed_networks.definitions import POSITIVE_LINK, NEGATIVE_LINK, NO_LINK
from project.util import memoize

__author__ = 'abinesh'

class RandomLinkGenerator:
    def __init__(self, positive, negative):
        self.total_positive = positive
        self.total_negative = negative

        self.assigned_positive = 0
        self.assigned_negative = 0

    def __random_pick(self, list, probabilities):
        x = uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(list, probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: break
        return item

    @memoize
    def next_random(self, pair):
        # argument 'pair' is used for memoization
        remaining_positive = self.total_positive - self.assigned_positive
        remaining_negative = self.total_negative - self.assigned_negative
        total_remaining = remaining_positive + remaining_negative
        retval = self.__random_pick([POSITIVE_LINK, NEGATIVE_LINK],
            [1.0 * remaining_positive / total_remaining, 1.0 * remaining_negative / total_remaining])
        if retval == POSITIVE_LINK: self.assigned_positive += 1
        if retval == NEGATIVE_LINK: self.assigned_negative += 1
        return retval


class RandomNetwork:
    def __init__(self, positive, negative, definition, def_args):
        self.generator = RandomLinkGenerator(positive, negative)
        self.definition = definition
        self.def_args = def_args

    def link_sign(self, data, year, A, B, def_args):
        assert self.def_args == def_args
        return self.generator.next_random(sorted([A, B])) if self.definition(data, year, A, B, def_args) != NO_LINK\
        else NO_LINK


def count_edge_types(data, year, definition, def_args):
    no_edge_count, positive_edges_count, negative_edges_count = 0, 0, 0
    for (A, B) in combinations(data.countries(), 2):
        link_type = definition(data, year, A, B, def_args)
        if link_type == NEGATIVE_LINK: negative_edges_count += 1
        elif link_type == POSITIVE_LINK: positive_edges_count += 1
        elif link_type == NO_LINK: no_edge_count += 1
    return no_edge_count, positive_edges_count, negative_edges_count