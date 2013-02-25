from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import args_for_definition_B, definition_B, POSITIVE_LINK, NEGATIVE_LINK
from project.structural_balance.plots.config import OUT_DIR

def print_graph_densities_for_different_sliding_windows(data, sliding_window_sizes, years):
    f = open(OUT_DIR.DEFINITION_B + 'combinations.txt', 'w')
    for T in sliding_window_sizes:
        args = args_for_definition_B(T, f)
        for year in years:
            positive_edges = 0
            negative_edges = 0
            for (A, B) in countries.country_pairs(data.countries()):
                link_sign = definition_B(data, year, A, B, args)
                if link_sign == POSITIVE_LINK: positive_edges += 1
                if link_sign == NEGATIVE_LINK: negative_edges += 1
            N = 203
            density = 2.0 * (positive_edges + negative_edges) / (N * (N - 1)) * 100
            print "%d,%d,%f,%d,%d,%d" % (T, year, density, positive_edges, negative_edges, N)
    f.close()

data = ExportData(start_year=1966, end_year=1969)
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

print_graph_densities_for_different_sliding_windows(data, [5, 6, 7, 8, 9, 10],
    [1969, 1979, 1988, 1989, 1990, 1999, 2000])