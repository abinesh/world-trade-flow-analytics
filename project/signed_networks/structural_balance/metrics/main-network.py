from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C, POSITIVE_LINK, NEGATIVE_LINK
from project.signed_networks.structural_balance.metrics.network import print_table, table1, link_type_ratio, traid_type_ratio


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

year = 2000

definition = definition_C3
def_args1000 = args_for_definition_C(10, 1000)
def_args5000 = args_for_definition_C(10, 5000)

# print_table(table1(data, year, definition, def_args1000))

def print_code_for_sign_distribution_over_time():
    print "x=%s;" % str([year for year in data.all_years]).replace(",", " ")
    print "p1000=%s;" % str([link_type_ratio(data, year, definition, def_args1000, POSITIVE_LINK)
                             for year in data.all_years]).replace(",", " ")
    print "p5000=%s;" % str([link_type_ratio(data, year, definition, def_args5000, POSITIVE_LINK)
                             for year in data.all_years]).replace(",", " ")
    print "n1000=%s;" % str([link_type_ratio(data, year, definition, def_args1000, NEGATIVE_LINK)
                             for year in data.all_years]).replace(",", " ")
    print "n5000=%s;" % str([link_type_ratio(data, year, definition, def_args5000, NEGATIVE_LINK)
                             for year in data.all_years]).replace(",", " ")
    print "plot(x,p1000,x,p5000,x,n1000,x,n5000);"
    print "legend('positive(1000)','positive(5000)','negative(1000)','negative(5000)')"
    print "saveas(gcf,'sign-distribution-over-time(Not-density)','png');"


def print_code_for_triad_distribution_over_time(def_args, file_name):
    print "x=%s;" % str([year for year in data.all_years]).replace(",", " ")
    print "t0=%s;" % str([traid_type_ratio(data, year, definition, def_args, 'T0')
                          for year in data.all_years]).replace(",", " ")
    print "t1=%s;" % str([traid_type_ratio(data, year, definition, def_args, 'T1')
                          for year in data.all_years]).replace(",", " ")
    print "t2=%s;" % str([traid_type_ratio(data, year, definition, def_args, 'T2')
                          for year in data.all_years]).replace(",", " ")
    print "t3=%s;" % str([traid_type_ratio(data, year, definition, def_args, 'T3')
                          for year in data.all_years]).replace(",", " ")
    print "plot(x,t0,x,t1,x,t2,x,t3);"
    print "legend('T0','T1','T2','T3')"
    print "saveas(gcf,'traid-distribution-over-time(Not-clustering-coefficient)-%s','png');" % file_name


# print_code_for_sign_distribution_over_time()
print_code_for_triad_distribution_over_time(def_args1000, '1000')
print_code_for_triad_distribution_over_time(def_args5000, '5000')