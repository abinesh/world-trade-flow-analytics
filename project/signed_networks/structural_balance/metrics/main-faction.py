from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C, POSITIVE_LINK, NEGATIVE_LINK
from project.signed_networks.structural_balance.metrics.faction import detect_factions_from_co_movements
from project.signed_networks.structural_balance.metrics.vertex import edge_count

data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_C3
def_args = args_for_definition_C(10, 5000)
window_size = 3

map_data = {}
for year in data.all_years:
    print "processing year %d" % year
    map_data[year] = {
        country: (
            edge_count(country, data, def_args, definition_C3, year, POSITIVE_LINK),
            edge_count(country, data, def_args, definition_C3, year, NEGATIVE_LINK
            )
        )
        for country in data.countries()
    }

print "done with constructing map_data"

for year in range(data.all_years[0] + window_size, data.all_years[-1] + 1):
    print "%d:%s" % (year, detect_factions_from_co_movements(map_data, window_size, year))