from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.structural_balance.metrics.vertex import degree_sum, degree_count, positive_edge_count, negative_edge_count
from project.util import file_safe

data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_C3
def_args1 = args_for_definition_C(10, 5000)
def_args2 = args_for_definition_C(10, 1000)


def print_degree_sum_over_time(args, other_args, this, other):
    print "x=%s;" % str([year for year in data.all_years]).replace(",", " ")
    for A in data.countries():
        print "degreecount=%s;" % str([degree_count(data, year, A, definition, args) for year in data.all_years]).replace(",", " ")
        print "degreesum1=%s;" % str([degree_sum(data, year, A, definition, args) for year in data.all_years]).replace(",", " ")
        print "positivecount1=%s;" % str([positive_edge_count(data, year, A, definition, args) for year in data.all_years]).replace(",", " ")
        print "negativecount1=%s;" % str([negative_edge_count(data, year, A, definition, args) for year in data.all_years]).replace(",", " ")
        print "degreesum2=%s;" % str([degree_sum(data, year, A, definition, other_args) for year in data.all_years]).replace(",", " ")
        print "plot(x,degreesum1,'b-o',x,degreesum2,'b-*',x,degreecount,'m-o',x,positivecount1,'g-o',x,negativecount1,'r-o');"
        print "hline = refline([0 0]);"
        print "set(hline,'Color','b');"
        print "legend('degree-sum1(T2=%d)','degree-sum2(T2=%d)','degree-count','positivecount1','negativecount1','Location','Best')" %(this,other)
        print "saveas(gcf,'%s-%d','png');" % (file_safe(A),this)


print_degree_sum_over_time(def_args1, def_args2, 5000, 1000)
print_degree_sum_over_time(def_args2, def_args1, 1000, 5000)