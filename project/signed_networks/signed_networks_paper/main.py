#Implementation of tables listed in paper http://www.cs.cornell.edu/home/kleinber/chi10-signed.pdf
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C1, args_for_definition_C, definition_C2, definition_D, args_for_definition_D, definition_A, definition_B, args_for_definition_A, args_for_definition_B
from project.signed_networks.signed_networks_paper.tables import table1

data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

print "FIX THIS: def_A number of traids is not correct: Expected 1373701, actual:1394237.8333333333"
print table1(data, 2000, definition_A, args_for_definition_A(.5, 2))
print table1(data, 2000, definition_B, args_for_definition_B(5))
print table1(data, 2000, definition_C1, args_for_definition_C(5000, 1))
print table1(data, 2000, definition_C2, args_for_definition_C(10, 1))
print table1(data, 2000, definition_D, args_for_definition_D(90))
