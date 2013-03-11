from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import country_pairs
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import args_for_definition_B, definition_B, POSITIVE_LINK, definition_C3, args_for_definition_C, NO_LINK
from project.signed_networks.structural_balance.config import html_header, html_footer, output_file_html


def normalize(n):
#    normalizes 0.5 to 2 to a repulsion percentage. 1 returns 0% repulsion, and it grows on either side of 1 with 0.5 and 2 returning 100%
    if n == 0: return 1
    if n < 1:
        n = 1 / n
    return n - 1


def generate_network_graph_data(data, year, subset_of_countries, out_file, definition, args):
    f = open(out_file, 'w')
    f.write(html_header())
    for (c1, c2) in country_pairs(subset_of_countries):
        link_type = definition(data, year, c1, c2, args)
        if link_type != NO_LINK:
            ratio = data.export_import_ratio(c1, c2, year)
            f.write('{source:"%s", target:"%s", type:"%s",repulsionpercentage:"%f"},\n' % (
                c1, c2, link_type, normalize(ratio)))

    f.write(html_footer(year))
    f.close()


data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

for year in range(1968, 2001):
    top_countries_and_exports = data.top_countries_by_export(year, 100)
    # top_countries_and_exports = data.countries()
    generate_network_graph_data(data, year, top_countries_and_exports, output_file_html(year),
                                definition_C3,
                                args_for_definition_C(10, 5000))

