from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData

from project.signed_networks.definitions import definition_C3, args_for_definition_C, POSITIVE_LINK, NO_LINK, NEGATIVE_LINK
from project.signed_networks.structural_balance.metrics.network import print_table, table1, link_type_ratio


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

year = 2000

definition = definition_C3
def_args1000 = args_for_definition_C(10, 1000)
def_args5000 = args_for_definition_C(10, 5000)

# print_table(table1(data, year, definition, def_args1000))

print "x=%s;" % str([year for year in data.all_years]).replace(",", " ")
print "p1000=%s;" % str([link_type_ratio(data, year, definition, def_args1000, POSITIVE_LINK)
                         for year in data.all_years]).replace(",", " ")
print "p5000=%s;" % str([link_type_ratio(data, year, definition, def_args5000, POSITIVE_LINK)
                         for year in data.all_years]).replace(",", " ")
print "n1000=%s;" % str([link_type_ratio(data, year, definition, def_args1000, NEGATIVE_LINK)
                         for year in data.all_years]).replace(",", " ")
print "n5000=%s;" % str([link_type_ratio(data, year, definition, def_args5000, NEGATIVE_LINK)
                         for year in data.all_years]).replace(",", " ")
print "m1000=%s;" % str([link_type_ratio(data, year, definition, def_args1000, NO_LINK)
                         for year in data.all_years]).replace(",", " ")
print "m5000=%s;" % str([link_type_ratio(data, year, definition, def_args5000, NO_LINK)
                         for year in data.all_years]).replace(",", " ")
print "plot(x,p1000,x,p5000,x,n1000,x,n5000,x,m1000,x,m5000);"
print "legend('positive(1000)','positive(5000)','negative(1000)','negative(5000)','missing(1000)','missing(5000)')"
print "saveas(gcf,'sign-distribution-over-time','png');"
