from itertools import combinations
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import  args_for_definition_C, POSITIVE_LINK, NEGATIVE_LINK, definition_C2, NO_LINK, definition_C1
from project.structural_balance.plots.config import OUT_DIR

def print_densities_for_thresholds(data, definition, T1_thresholds, combinations_file_name):
    f = open(OUT_DIR.DEFINITION_C + combinations_file_name + '-combinations.txt', 'w')

    for min_export_threshold in T1_thresholds:
        for percentage_threshold in [1]:
            for year in [1969, 1979, 1988, 1989, 1990, 1999, 2000]:
                (positive_edges, negative_edges) = (0, 0)
                for (A, B) in countries.country_pairs(data.countries()):
                    link_sign = definition(data, year, A, B,
                        args_for_definition_C(min_export_threshold, percentage_threshold, f))
                    if link_sign == POSITIVE_LINK: positive_edges += 1
                    if link_sign == NEGATIVE_LINK: negative_edges += 1
                N = 203
                density = 2.0 * (positive_edges + negative_edges) / (N * (N - 1)) * 100
                print "%d,%f,%d,%f,%d,%d,%d" % (
                    min_export_threshold, percentage_threshold, year, density, positive_edges, negative_edges, N)
    f.close()


def print_histogram_matlab_code(data, T):
    i = 0
    str = ""
    list = []
    for (A, B) in countries.country_pairs(data.countries()):
        total = data.total_exports_from_C1_to_C2(A, B)
        if total != 0 and total > T:
            str = "%s %d" % (str, total)
            list.append(total)
            i += 1
    print "y=[%s];" % str
    print "hist(y,100000);"
    print "xlabel('Export quantity');"
    print "ylabel('Count of country pairs');"
    print "set(gca, 'Xscale', 'log');"
    print "saveas(gcf,'definition_C_histogram','png');"


def print_traid_counts(data, definition):
    args = args_for_definition_C(1000, 1)
    for year in [1970, 1980, 1990, 2000]:
        t0, t1, t2, t3 = 0, 0, 0, 0
        for (A, B, C) in combinations(data.countries(), 3):
            side1 = definition(data, year, A, B, args)
            side2 = definition(data, year, B, C, args)
            side3 = definition(data, year, C, A, args)
            if side1 == NO_LINK or side2 == NO_LINK or side3 == NO_LINK: continue
            positive_sides = 0
            for side in [side1, side2, side3]:
                if side == POSITIVE_LINK: positive_sides += 1
            if positive_sides == 0: t0 += 1
            if positive_sides == 1: t1 += 1
            if positive_sides == 2: t2 += 1
            if positive_sides == 3: t3 += 1
        print "%d,t0=%d,t1=%d,t2=%d,t3=%d" % (year, t0, t1, t2, t3)

data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

#print_histogram_matlab_code(data, 1000)
print_densities_for_thresholds(data, definition_C1, [0, 100, 200, 250, 300, 500, 1000, 1500, 2000, 3000, 5000],
    'definition_C1')
#print_densities_for_thresholds(data, definition_C2, range(0, 2000 - 1963 + 1),'definition_C2')
#print_traid_counts(data, definition_C1)

