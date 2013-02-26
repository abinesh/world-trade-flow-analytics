import math
from numpy import average

__author__ = 'abinesh'

def column_to_year(column):
    if column == "Value00":
        return 2000
    return 1900 + int(column[5:])


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


def std_dev(s):
    if len(s) == 0: return None
    avg = sum(s) * 1.0 / len(s)
    variance = map(lambda x: (x - avg) ** 2, s)
    return math.sqrt(average(variance))
