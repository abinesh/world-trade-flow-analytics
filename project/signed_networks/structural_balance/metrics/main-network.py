from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.structural_balance.metrics.network import print_table, table1


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

year = 2000

print_table(table1(data, year, definition_C3, args_for_definition_C(10, 5000)))