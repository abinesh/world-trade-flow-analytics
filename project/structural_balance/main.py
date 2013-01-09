from project.config import  WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import country_pairs
from project.export_data.exportdata import ExportData
from project.structural_balance.config import  output_file_html, html_footer, html_header
from project.structural_balance.definitions import  NO_LINK, args_for_definition_B, definition_B, POSITIVE_LINK

def normalize(n):
    if n < 1:
        n = 1 / n
    return  n - 1

def generate_network_graph_data(data, year, subset_of_countries, out_file, definition, args):

    f = open(out_file, 'w')
    f.write(html_header)
    for (c1, c2) in country_pairs(subset_of_countries):
        link_type = definition(data, year, c1, c2, args)
        if link_type != NO_LINK:
            ratio = data.export_import_ratio(c1, c2, year)
            f.write('{source:"%s", target:"%s", type:"%s",repulsionpercentage:"%f"},\n' % (
                    c1, c2, link_type, normalize(ratio)))

    f.write(html_footer)
    f.close()

data = ExportData()
data.load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

for year in range(1968, 2001):
    top_countries_and_exports = data.top_countries_by_export(year, 50)
    generate_network_graph_data(data, year, top_countries_and_exports, output_file_html(year),
        definition_B,
        args_for_definition_B(5))

