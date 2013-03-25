from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import world_excluded_countries_list
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C, POSITIVE_LINK, NEGATIVE_LINK
from project.signed_networks.structural_balance.metrics.faction import positives_and_negatives_matrix_matlab, adjacency_matrix_matlab

data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_C3
def_args = args_for_definition_C(10, 5000)

print "xpn=[%s]" % positives_and_negatives_matrix_matlab(data, definition, def_args, [1981, 1982, 1983, 1984])
print "xad=[%s]" % adjacency_matrix_matlab(data, definition, def_args, 1982,world_excluded_countries_list())

def print_adjacency_matrix_row(A,year):
    print str([("0" if A == B else "1" if definition(data, year, A, B, def_args) == POSITIVE_LINK
    else "-1" if definition(data, year, A, B, def_args) == NEGATIVE_LINK else "0")
           for B in data.countries()]) \
    .replace(",", " ").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "")

print_adjacency_matrix_row("China",1970)
print_adjacency_matrix_row("China",1990)

