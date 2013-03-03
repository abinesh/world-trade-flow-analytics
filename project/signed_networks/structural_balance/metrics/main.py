from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C1, args_for_definition_C, definition_C2, definition_D, args_for_definition_D, definition_B, args_for_definition_B, definition_C3
from project.signed_networks.structural_balance.metrics.edge import fraction_of_embedded_positive_signs, max_common_neighbours_possible, traids_per_common_edge_count
from project.signed_networks.structural_balance.metrics.network import table2, print_table
from project.signed_networks.structural_balance.metrics.util import RandomNetwork, count_edge_types


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

year = 1964
#for table in [table2]:
#    print_table(table(data, year, definition_B, args_for_definition_B(5)))
#    print_table(table(data, year, definition_C1, args_for_definition_C(5000, 0.01)))
#    print_table(table(data, year, definition_C2, args_for_definition_C(10, 0.01)))
#    print_table(table(data, year, definition_C3, args_for_definition_C(10, 5000)))
#    print_table(table(data, year, definition_D, args_for_definition_D(90)))
#    print_table(table(data, year, definition_D, args_for_definition_D(99)))

#fractions = fraction_of_embedded_positive_signs(data, year, definition_C3, args_for_definition_C(10, 5000))
(_, positive_edges, negative_edges) = count_edge_types(data, year, definition_C3, args_for_definition_C(10, 5000))
randomNetwork = RandomNetwork(positive_edges, negative_edges, definition_C3, args_for_definition_C(10, 5000))
#random_fractions = fraction_of_embedded_positive_signs(data, year, randomNetwork.link_sign,
#    args_for_definition_C(10, 5000))

#for i in range(0, max_common_neighbours_possible + 1):
#    print "%d\t%.5f\t%.5f" % (i, fractions[i], random_fractions[i])

traid_counts = traids_per_common_edge_count(data, year, definition_C3, args_for_definition_C(10, 5000))
rtraid_counts = traids_per_common_edge_count(data, year, randomNetwork.link_sign, args_for_definition_C(10, 5000))

for i in range(0, max_common_neighbours_possible + 1):
    (t0, t1, t2, t3) = traid_counts[i]
    (rt0, rt1, rt2, rt3) = rtraid_counts[i]
    print "%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d" % (i, t0, rt0, i, t1, rt1, i, t2, rt2, i, t3, rt3)
