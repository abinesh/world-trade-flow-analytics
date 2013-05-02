from copy import deepcopy
import math
from numpy import average


def column_to_year(column): return 2000 if column == "Value00" else 1900 + int(column[5:])


def memoize(function):
    memo = {}

    def wrapper(*args):
        key = str(args)
        if key in memo:
            return memo[key]
        else:
            rv = function(*args)
            memo[key] = rv
            return rv

    return wrapper


def file_safe(country):
#    strip('. ,') trims whitespaces, periods and comma characters
    return country.strip('. ,').replace(',', '_').replace('.', '_').replace(' ', '_')


def transpose(matrix): return [list(i) for i in zip(*matrix)]


def std_dev(s):
    if len(s) == 0: return None
    avg = sum(s) * 1.0 / len(s)
    variance = map(lambda x: (x - avg) ** 2, s)
    return math.sqrt(average(variance))


def fraction(numerator, denominator, nan_value): return nan_value if denominator == 0 else numerator * 1.0 / denominator


class Counts:
    def __init__(self):
        self.as_map_var = {0: 0}

    def record(self, count):
        if count not in self.as_map_var: self.as_map_var[count] = 0
        self.as_map_var[count] += 1

    def as_map(self):
        copied_map = deepcopy(self.as_map_var)
        del copied_map[0]
        return copied_map

    def as_tuples_list(self):
        copied_map = self.as_map()
        sorted_sparse_tuples_list = sorted([(key, copied_map[key]) for key in copied_map],
                                           key=lambda key_value: key_value[0])
        return_list = []
        index = 1
        lag_index = 0
        last_index = sorted_sparse_tuples_list[-1:][0][0]
        while index - 1 < last_index:
            t = sorted_sparse_tuples_list[index - lag_index - 1]
            if t[0] == index:
                return_list.append(t)
            else:
                return_list.append((index, 0))
                lag_index += 1
            index += 1

        return return_list

