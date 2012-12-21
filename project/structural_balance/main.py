from project.config import  WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import country_pairs, a_subset_of_countries, world_excluded_countries_list
from project.export_data.exportdata import ExportData
from project.structural_balance.config import output_file, output_file_html, html_footer, html_header
from project.structural_balance.definitions import definition_A, NO_LINK, args_for_definition_A, args_for_definition_B, definition_B
from project.traids_vs_degree_plot.config import STRONG_TIES_LOWER_BOUND, STRONG_TIES_UPPER_BOUND

def generate_network_graph_data(data, year, subset_of_countries, out_file, definition, args):
    f = open(out_file, 'w')
    f.write(html_header)
    for (c1, c2) in country_pairs(subset_of_countries):
        link_type = definition(data, year, c1, c2, args)
        if link_type != NO_LINK:
            f.write('{source:"%s", target:"%s", type:"%s"},\n' % (c1, c2, link_type))

    f.write(html_footer)
    f.close()

data = ExportData()
data.load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

#generate_network_graph_data(data, 2000, a_subset_of_countries, output_file(2000), definition_A,
#    args_for_definition_A(STRONG_TIES_LOWER_BOUND, STRONG_TIES_UPPER_BOUND))

for year in range(1968, 2001):
    top_countries_and_exports = data.top_countries_by_export(year, 50)
    generate_network_graph_data(data, year, top_countries_and_exports, output_file_html(year),
        definition_B,
        args_for_definition_B(5))

