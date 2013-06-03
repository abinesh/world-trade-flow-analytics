from itertools import combinations
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C

data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

year = 1975
definition = definition_C3
args = args_for_definition_C(10, 5000)

for (A, B) in combinations(data.countries(), 2):
    print "%s,%s,%s" % (A, B, definition(data, year, A, B, args))
