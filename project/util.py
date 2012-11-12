__author__ = 'abinesh'

def column_to_year(column):
    if column == "Value00":
        return 2000
    return 1900 + int(column[5:])