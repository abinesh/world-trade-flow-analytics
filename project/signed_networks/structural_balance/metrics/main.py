from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C1, args_for_definition_C, definition_C2, definition_D, args_for_definition_D, definition_B, args_for_definition_B, definition_C3
from project.signed_networks.structural_balance.metrics.edge import fraction_of_embedded_positive_signs, max_common_neighbours_possible
from project.signed_networks.structural_balance.metrics.network import table2, print_table


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

#for table in [table2]:
#    print_table(table(data, 2000, definition_B, args_for_definition_B(5)))
#    print_table(table(data, 2000, definition_C1, args_for_definition_C(5000, 0.01)))
#    print_table(table(data, 2000, definition_C2, args_for_definition_C(10, 0.01)))
#    print_table(table(data, 2000, definition_C3, args_for_definition_C(10, 5000)))
#    print_table(table(data, 2000, definition_D, args_for_definition_D(90)))
#    print_table(table(data, 2000, definition_D, args_for_definition_D(99)))

fractions = fraction_of_embedded_positive_signs(data, 2000, definition_C3, args_for_definition_C(10, 5000))

for i in range(0, max_common_neighbours_possible + 1):
    print "%d\t%.5f" % (i, fractions[i])
