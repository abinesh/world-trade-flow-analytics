from numpy import corrcoef
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.structural_balance.metrics.config import OUT_DIR
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

def transform_pn_to_01(matrix, threshold):
    return [(1 if cell > threshold else 0 for cell in row) for row in matrix]


def write_matlab_code_for_rcm(data, definition, def_args):
    f = open(OUT_DIR.RCM_MATRIC + 'code.txt', 'w')
    for year in [1965, 1970, 1975, 1980, 1985, 1990, 1995, 1999, 2000]:
        corrcoef_mat = corrcoef(adjacency_matrix(data, definition, def_args, year))
        for coeff in range(0, 11):
            c = coeff * .05
            f.write(corrcoef_py_to_matlab('c0', transform_pn_to_01(corrcoef_mat, c)) + "\n")
            f.write("r = symrcm(c0);\n")
            f.write("spy(c0);\n")
            f.write("saveas(gcf,'%d-%d-unordered','png');\n" % (year, c * 100))
            f.write("spy(c0(r,r));\n")
            f.write("saveas(gcf,'%d-%d-ordered','png');\n" % (year, c * 100))
    f.close()

# print "countriesVector={'India','USA','UK','Germany'};"
# print "HeatMap(-corrmatrix,'RowLabels',countriesVector,'ColumnLabels',countriesVector, 'Colormap', redgreencmap(200))"
# print "HeatMap(-corrmatrix, 'Colormap', redgreencmap(200))"

# print corrcoef_py_to_matlab('corrmatrix', corrcoef(adjacency_matrix(data, definition, def_args, 1990)))
# print "countriesVector={'India','USA','UK','Germany'};"
# print "HeatMap(-corrmatrix,'RowLabels',countriesVector,'ColumnLabels',countriesVector, 'Colormap', redgreencmap(200))"
# print "HeatMap(-corrmatrix, 'Colormap', redgreencmap(200))"

def write_correlation_list(file_name, matrix, threshold):
    f = open(OUT_DIR.CORRELATION_LIST + file_name, 'w')
    count = 0
    for row in detect_community(corrcoef(matrix), threshold):
        f.write("%d:%s,%d,%s\n" % (count, countries.index_to_country_map[count], len(row), row))
        count += 1
    f.close()


def write_all_correlation_files(data, definition, def_args):
    window_size = 4
    for year in data.all_years:
        write_correlation_list('adj-y%d.txt' % year, adjacency_matrix(data, definition, def_args, year), 0)
        if 1963 + window_size <= year:
            write_correlation_list('pn-y%d-to-y%d.txt' % (year - window_size + 1, year),
                                   positives_and_negatives_matrix(data, definition, def_args,
                                                                  range(year - window_size + 1, year + 1)), 0.5)


# write_all_correlation_files(data, definition, def_args)
write_matlab_code_for_rcm(data, definition, def_args)


