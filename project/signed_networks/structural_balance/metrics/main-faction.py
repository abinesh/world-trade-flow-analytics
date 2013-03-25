from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.structural_balance.metrics.faction import positives_and_negatives_matrix, adjacency_matrix

data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_C3
def_args = args_for_definition_C(10, 5000)


falklands_war_countries = ["USA", "UK", "Argentina", "France,Monac", "Libya", "Fm USSR", "Israel", "Peru", "Brazil"]

print "xpn=[%s]" % positives_and_negatives_matrix(data, definition, def_args, [1981, 1982, 1983, 1984],
                                                  falklands_war_countries)
print "xad=[%s]" % adjacency_matrix(data, definition, def_args, 1982, falklands_war_countries)
