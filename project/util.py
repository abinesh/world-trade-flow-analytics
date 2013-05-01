import math
from numpy import average

__author__ = 'abinesh'


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
        self.as_map = {}

    def record(self, count):
        if count not in self.as_map: self.as_map[count] = 0
        self.as_map[count] += 1

    def asMap(self):
        return self.as_map
