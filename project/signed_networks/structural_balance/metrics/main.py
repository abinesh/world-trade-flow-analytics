from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C1, args_for_definition_C, definition_C2, definition_D, args_for_definition_D, definition_B, args_for_definition_B, definition_C3
from project.signed_networks.structural_balance.metrics.edge import fraction_of_embedded_positive_signs, max_common_neighbours_possible, traids_per_common_edge_count
from project.signed_networks.structural_balance.metrics.network import table2, print_table
from project.signed_networks.structural_balance.metrics.util import RandomNetwork, count_edge_types


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

year = 2000
#for table in [table2]:
#    print_table(table(data, year, definition_B, args_for_definition_B(5)))
#    print_table(table(data, year, definition_C1, args_for_definition_C(5000, 0.01)))
#    print_table(table(data, year, definition_C2, args_for_definition_C(10, 0.01)))
#    print_table(table(data, year, definition_C3, args_for_definition_C(10, 5000)))
#    print_table(table(data, year, definition_D, args_for_definition_D(90)))
#    print_table(table(data, year, definition_D, args_for_definition_D(99)))
def print_embeddedness_matlab_code():
    common_neighbours_range = range(0, max_common_neighbours_possible + 1)
    print "x=%s" % (str(common_neighbours_range).replace(",", " "))
    args = args_for_definition_C(10, 5000)
    for year in data.all_years:
        fractions = fraction_of_embedded_positive_signs(data, year, definition_C3, args)
        (_, positive_edges, negative_edges) = count_edge_types(data, year, definition_C3, args)
        randomNetwork = RandomNetwork(positive_edges, negative_edges, definition_C3, args)
        random_fractions = fraction_of_embedded_positive_signs(data, year, randomNetwork.link_sign, args)

        print "actual=%s" % (str([fractions[i] for i in common_neighbours_range]).replace(",", " "))
        print "random=%s" % (str([random_fractions[i] for i in common_neighbours_range]).replace(",", " "))
        print "plot(x,actual,'b-*',x,random,'r-*');"
        print "saveas(gcf,'link-embeddedness-%s','png');" % year

#traid_counts = traids_per_common_edge_count(data, year, definition_C3, args_for_definition_C(10, 5000))
#
#for i in range(0, max_common_neighbours_possible + 1):
#    (t0, t1, t2, t3) = traid_counts[i]
#    print "%d\t%d\t%d\t%d\t%d" % (i, t0, t1, t2, t3)

print_embeddedness_matlab_code()
