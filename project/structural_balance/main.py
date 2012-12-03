from project import countries
from project.config import  WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import country_pairs
from project.traids_vs_degree_plot.config import STRONG_TIES_LOWER_BOUND, STRONG_TIES_UPPER_BOUND
from project.traids_vs_degree_plot.export_data.exportdata import load_export_data, export_data
from project.traids_vs_degree_plot.export_data.strongties import is_there_a_strong_tie_method_B

load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

def total_exports(exporter, year):
    return export_data(year, exporter, 'World')

count = 0
for (c1, c2) in country_pairs():
    if count == 2000:
        break
    type = "suit" if is_there_a_strong_tie_method_B(2000, c1, c2, STRONG_TIES_LOWER_BOUND,
        STRONG_TIES_UPPER_BOUND) else "resolved"
    print   '{source:"%s", target:"%s", type:"%s"},' % (c1, c2, type)
    count += 1
    pass
