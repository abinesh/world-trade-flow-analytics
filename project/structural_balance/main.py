from project.config import  WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import country_pairs, a_subset_of_countries
from project.export_data.exportdata import ExportData
from project.export_data.strongties import is_there_a_strong_tie_method_B
from project.structural_balance.config import output_file
from project.traids_vs_degree_plot.config import STRONG_TIES_LOWER_BOUND, STRONG_TIES_UPPER_BOUND


def generate_network_graph_data_for_structured_balance_definition_A(data, year, only_these_countries, out_file):
    f = open(out_file, 'w')
    for (c1, c2) in country_pairs(only_these_countries):
        type = "suit" if is_there_a_strong_tie_method_B(data, year, c1, c2, STRONG_TIES_LOWER_BOUND,
            STRONG_TIES_UPPER_BOUND) else "resolved"
        f.write('{source:"%s", target:"%s", type:"%s"},\n' % (c1, c2, type))
    f.close()

data = ExportData()
data.load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

generate_network_graph_data_for_structured_balance_definition_A(data, 2000, a_subset_of_countries, output_file(2000))
