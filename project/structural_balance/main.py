from project.config import  WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import country_pairs, a_subset_of_countries
from project.export_data.exportdata import ExportData
from project.structural_balance.config import output_file
from project.structural_balance.definitions import definition_A


def generate_network_graph_data_for_structured_balance_definition_A(data, year, subset_of_countries, out_file):
    f = open(out_file, 'w')
    for (c1, c2) in country_pairs(subset_of_countries):
        f.write('{source:"%s", target:"%s", type:"%s"},\n' % (c1, c2, definition_A(c1, c2, data, year)))
    f.close()

data = ExportData()
data.load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

generate_network_graph_data_for_structured_balance_definition_A(data, 2000, a_subset_of_countries, output_file(2000))
