from itertools import combinations
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import  args_for_definition_C, POSITIVE_LINK, NEGATIVE_LINK, definition_C2, NO_LINK, definition_C1, definition_C3, definition_D, args_for_definition_D
from project.structural_balance.plots.config import OUT_DIR

def print_densities_for_thresholds(data, definition, T1_thresholds, T2_thresholds, log_file_name):
    f1 = open(OUT_DIR.DEFINITION_C + log_file_name + '-edges.txt', 'w')
    f2 = open(OUT_DIR.DEFINITION_C + log_file_name + '-traids.txt', 'w')
    f3 = open(OUT_DIR.DEFINITION_C + log_file_name + '-nodes.txt', 'w')
    countries_list = ['USA', 'Iran', 'Iraq', 'Argentina', 'UK', 'China', 'Kuwait', 'France,Monac']

    for pruning_T in T1_thresholds:
        for classifying_T in T2_thresholds:
            args1 = args_for_definition_C(pruning_T, classifying_T, f1)
            args2 = args_for_definition_C(pruning_T, classifying_T, f1)

            for year in range(1969, 2001):
                (positive_edges, negative_edges) = (0, 0)
                for (A, B) in countries.country_pairs(countries_list):
                    link_sign = definition(data, year, A, B, args1)
                    if link_sign == POSITIVE_LINK: positive_edges += 1
                    if link_sign == NEGATIVE_LINK: negative_edges += 1
                N = 203
                density = 2.0 * (positive_edges + negative_edges) / (N * (N - 1)) * 100
                print "%d,%f,%d,%f,%d,%d,%d" % (
                    pruning_T, classifying_T, year, density, positive_edges, negative_edges, N)
                for (A, B, C) in combinations(countries_list, 3):
                    linkAtoB = definition(data, year, A, B, args2)
                    linkBtoC = definition(data, year, B, C, args2)
                    linkCtoA = definition(data, year, C, A, args2)
                    triangle = [linkAtoB, linkBtoC, linkCtoA]
                    pcount = triangle.count(POSITIVE_LINK)
                    ncount = triangle.count(NEGATIVE_LINK)
                    mcount = triangle.count(NO_LINK)
                    f2.write("%d,%.2f,%d,%s,%s,%s,%s,%s,%s,T%d%d%d\n" % (
                        year, pruning_T, classifying_T, A, B, C, linkAtoB, linkBtoC, linkCtoA, pcount, ncount, mcount))
                for A in countries_list:
                    degree_sum = 0
                    for B in data.countries():
                        if A == B: continue
                        link_sign = definition(data, year, A, B, args1)
                        degree_sum += 1 if link_sign == POSITIVE_LINK else -1 if link_sign == NEGATIVE_LINK else 0
                    f3.write("%d,%s,%d\n" % (year, A, degree_sum))
    f1.close()
    f2.close()
    f3.close()


def print_histogram_matlab_code(data, low, high):
    i = 0
    str = ""
    list = []
    for (A, B) in countries.country_pairs(data.countries()):
        total = data.total_exports_from_C1_to_C2(A, B)
        if total != 0 and low < total < high:
            str = "%s %d" % (str, total)
            list.append(total)
            i += 1
    print "y=[%s];" % str
    print "hist(y,100000);"
    print "xlabel('Export quantity');"
    print "ylabel('Count of country pairs');"
    print "set(gca, 'Xscale', 'log');"
    print "saveas(gcf,'definition_C_histogram','png');"

data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

#print_histogram_matlab_code(data, 0, 1000)
#print_densities_for_thresholds(data, definition_C1, [0, 100, 200, 250, 300, 500, 1000, 1500, 2000, 3000, 5000], [0.01],
#    'definition_C1')
#print_densities_for_thresholds(data, definition_C2, range(0, 2000 - 1963 + 1), [0.01], 'definition_C2')
print_densities_for_thresholds(data, definition_C3, [0], [100], 'definition_C3-100')
print_densities_for_thresholds(data, definition_C3, [0], [1000], 'definition_C3-1000')
print_densities_for_thresholds(data, definition_C3, [0], [5000], 'definition_C3-5000')
#print_densities_for_thresholds(data, definition_D, [0], [99], 'definition_D-99')
#print_densities_for_thresholds(data, definition_D, [0], [90], 'definition_D-90')
#print_densities_for_thresholds(data, definition_D, [0], [85], 'definition_D-85')

#print_densities_for_thresholds(data, definition_C2, [10], [0.01], 'definition_C2-001')
#print_densities_for_thresholds(data, definition_C2, [10], [0.1], 'definition_C2-01')
#print_densities_for_thresholds(data, definition_C2, [10], [1], 'definition_C2-1')
