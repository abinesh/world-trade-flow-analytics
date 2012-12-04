from project.config import  WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import country_pairs
from project.structural_balance.config import output_file
from project.traids_vs_degree_plot.config import STRONG_TIES_LOWER_BOUND, STRONG_TIES_UPPER_BOUND
from project.traids_vs_degree_plot.export_data.exportdata import load_export_data, export_data
from project.traids_vs_degree_plot.export_data.strongties import is_there_a_strong_tie_method_B

load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

def total_exports(exporter, year):
    return export_data(year, exporter, 'World')


def generate_network_graph_data_for_structured_balance(year, only_these_countries, out_file):
    f = open(out_file, 'w')
    for (c1, c2) in country_pairs(only_these_countries):
        type = "suit" if is_there_a_strong_tie_method_B(year, c1, c2, STRONG_TIES_LOWER_BOUND,
            STRONG_TIES_UPPER_BOUND) else "resolved"
        f.write('{source:"%s", target:"%s", type:"%s"},\n' % (c1, c2, type))
    f.close()

only_these = ["USA",
              "Afghanistan",
              "Africa N.NES",
              "Argentina",
              "Australia",
              "Austria",
              "Bahamas",
              "Bahrain",
              "Bangladesh",
              "Barbados",
              "Belgium-Lux",
              "Brazil",
              "Bulgaria",
              "Canada",
              "Chile",
              "China",
              "Colombia",
              "Congo",
              "Czechoslovak",
              "Denmark",
              "Ecuador",
              "Egypt",
              "Ethiopia",
              "Finland",
              "Fm USSR",
              "Fm Yemen AR",
              "Fm Yemen Ar",
              "Fm Yemen Dm",
              "Fm Yugoslav",
              "Fr Ind O",
              "Fr.Guiana",
              "France,Monac",
              "Georgia",
              "Germany",
              "Greece",
              "Greenland",
              "Guinea",
              "Hungary",
              "Iceland",
              "India",
              "Indonesia",
              "Iran",
              "Iraq",
              "Ireland",
              "Israel",
              "Italy",
              "Jamaica",
              "Japan",
              "Kenya",
              "Korea Rep.",
              "Kuwait",
              "Lebanon",
              "Libya",
              "Madagascar",
              "Malaysia",
              "Mauritius",
              "Mexico",
              "Mongolia",
              "Morocco",
              "Mozambique",
              "Myanmar",
              "Nepal",
              "Netherlands",
              "New Zealand",
              "Pakistan",
              "Paraguay",
              "Peru",
              "Philippines",
              "Poland",
              "Portugal",
              "Qatar",
              "Romania",
              "Russian Fed",
              "Saudi Arabia",
              "Singapore",
              "South Africa",
              "Spain",
              "Sri Lanka",
              "Sweden",
              "Switz.Liecht",
              "Taiwan",
              "Thailand",
              "Turkey",
              "UK",
              "Uganda",
              "Untd Arab Em",
              "Uruguay",
              "Viet Nam",
              "China FTZ"]
generate_network_graph_data_for_structured_balance(2000, only_these, output_file(2000))