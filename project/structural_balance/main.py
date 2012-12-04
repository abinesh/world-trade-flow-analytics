from project.config import  WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import country_pairs
from project.structural_balance.config import output_file
from project.traids_vs_degree_plot.config import STRONG_TIES_LOWER_BOUND, STRONG_TIES_UPPER_BOUND
from project.traids_vs_degree_plot.export_data.exportdata import load_export_data, export_data
from project.traids_vs_degree_plot.export_data.strongties import is_there_a_strong_tie_method_B

load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

def total_exports(exporter, year):
    return export_data(year, exporter, 'World')


def generate_network_graph_data_for_structured_balance(year, max_country_pairs,out_file):
    f = open(out_file, 'w')
    count = 0
    for (c1, c2) in country_pairs():
        if count == max_country_pairs:
            break
        type = "suit" if is_there_a_strong_tie_method_B(year, c1, c2, STRONG_TIES_LOWER_BOUND,
            STRONG_TIES_UPPER_BOUND) else "resolved"
        f.write('{source:"%s", target:"%s", type:"%s"},\n' % (c1, c2, type))
        count += 1
    f.close()

generate_network_graph_data_for_structured_balance(2000, -1, output_file(2000))