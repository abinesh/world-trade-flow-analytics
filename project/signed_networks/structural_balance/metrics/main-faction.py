from numpy import corrcoef
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import world_excluded_countries_list
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C, POSITIVE_LINK, NEGATIVE_LINK
from project.signed_networks.structural_balance.metrics.faction import positives_and_negatives_matrix_matlab, adjacency_matrix_matlab, positives_and_negatives_matrix, adjacency_matrix, adjacency_matrix_row
from project.util import transpose

data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_C3
def_args = args_for_definition_C(10, 5000)

print "xpn=[%s]" % positives_and_negatives_matrix_matlab(data, definition, def_args, [1981, 1982, 1983, 1984])
print "xad=[%s]" % adjacency_matrix_matlab(data, definition, def_args, 1982, world_excluded_countries_list())
print corrcoef(transpose(positives_and_negatives_matrix(data, definition, def_args, [1981, 1982, 1983, 1984])))
print corrcoef(adjacency_matrix(data, definition, def_args, 1982, world_excluded_countries_list()))
print adjacency_matrix_row(data, definition, def_args, 1970, "China")
print adjacency_matrix_row(data, definition, def_args, 1990, "China")

