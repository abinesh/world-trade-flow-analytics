from numpy import corrcoef
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.structural_balance.metrics.faction import positives_and_negatives_matrix_matlab, adjacency_matrix_matlab, positives_and_negatives_matrix, adjacency_matrix, adjacency_matrix_row, corrcoef_py_to_matlab
from project.util import transpose


def detect_community(correlation, threshold):
    result = []
    for i in range(0, len(correlation)):
        community = sorted([(countries.index_to_country_map[j], correlation[i][j])
                            for j in range(0, len(correlation)) if i != j and correlation[i][j] > threshold],
                           key=lambda t: -t[1])
        result.append([(a, float("%.2f" % b)) for (a, b) in community])
    return result


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_C3
def_args = args_for_definition_C(10, 5000)

# print "xpn=[%s]" % positives_and_negatives_matrix_matlab(data, definition, def_args, [1981, 1982, 1983, 1984])
# print "xpn=[%s]" % adjacency_matrix_matlab(data, definition, def_args, 1980)
# print corrcoef(adjacency_matrix(data, definition, def_args, 1980))

# print corrcoef(transpose(positives_and_negatives_matrix(data, definition, def_args, [1981, 1982, 1983, 1984])))

'''
print "xad=[%s]" % adjacency_matrix_matlab(data, definition, def_args, 1982)
print corrcoef(adjacency_matrix(data, definition, def_args, 1982))

print adjacency_matrix_row(data, definition, def_args, 1970, "China")
print adjacency_matrix_row(data, definition, def_args, 1990, "China")

print data.countries()
'''

# f=
# count = 0
# for row in detect_community(corrcoef(adjacency_matrix(data, definition, def_args, 1980)), 0):
# for row in detect_community(corrcoef(adjacency_matrix(data, definition, def_args, 1972)), 0):
# for row in detect_community(corrcoef(positives_and_negatives_matrix(data, definition, def_args, [1964,1965,1966,1967])),0.5):
# for row in detect_community(corrcoef(positives_and_negatives_matrix(data, definition, def_args, [1968,1969,1970,1971])),0.5):
# for row in detect_community(corrcoef(positives_and_negatives_matrix(data, definition, def_args, [1972,1973,1974,1975])),0.5):
#     print ("%d:%s,%d,%s" % (count, countries.index_to_country_map[count], len(row), row))
#     count += 1

# f.close()

print corrcoef_py_to_matlab('corrmatrix', corrcoef(adjacency_matrix(data, definition, def_args, 1980)))
print "countriesVector={'India','USA','UK','Germany'};"
# print "HeatMap(-corrmatrix,'RowLabels',countriesVector,'ColumnLabels',countriesVector, 'Colormap', redgreencmap(200))"
print "HeatMap(-corrmatrix, 'Colormap', redgreencmap(200))"



