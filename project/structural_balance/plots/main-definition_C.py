from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.structural_balance.definitions import definition_C, args_for_definition_C, POSITIVE_LINK, NEGATIVE_LINK
from project.structural_balance.plots.config import OUT_DIR

def print_densities_for_thresholds(data):
    min_export_threshold = 1000
    f = open(OUT_DIR.DEFINITION_C + 'combinations.txt', 'w')
    for percentage_threshold in [10, 5, 4, 3, 2, 1, 0.1]:
        for year in [1969, 1979, 1989, 1999, 2000]:
            unique_countries = {}
            (positive_edges, negative_edges) = (0, 0)
            for (A, B) in countries.country_pairs():
                link_sign = definition_C(data, year, A, B,
                    args_for_definition_C(min_export_threshold, percentage_threshold, f))
                if link_sign == POSITIVE_LINK:
                    positive_edges += 1
                    unique_countries[A] = 1
                    unique_countries[B] = 1
                if link_sign == NEGATIVE_LINK:
                    negative_edges += 1
                    unique_countries[A] = 1
                    unique_countries[B] = 1
            N = len(unique_countries)
            density = 2.0 * (positive_edges + negative_edges) / (N * (N - 1)) * 100
            print "%f,%d,%f,%d,%d,%d" % (percentage_threshold, year, density, positive_edges, negative_edges, N)
    f.close()


def print_total_exports(data):
    i = 0
    str = ""
    list = []
    for (A, B) in countries.country_pairs():
        total = data.total_exports_from_C1_to_C2(A, B)
        if total != 0:
            str = "%s %d" % (str, total)
            list.append(total)
            i += 1
    print str

data = ExportData()
data.load_export_data('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

#print_total_exports(data)
print_densities_for_thresholds(data)

