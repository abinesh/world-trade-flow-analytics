from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.link_prediction.link import percentage_of_new_edges_over_time, percentage_of_edge_sign_changes_over_time


def edge_proportion_over_time(data, definition, def_args, function, look_back_durations):
    for look_back_duration in look_back_durations:
        x_axis = data.all_years[look_back_duration:]
        print "x%d=%s;" % (look_back_duration, str(x_axis).replace(",", ""))
        print "y%d=%s;" % (look_back_duration, str(
            [function(data, definition, def_args, year, look_back_duration) for year in x_axis]).replace(",", ""))
    print "plot(x1,y1,x5,y5,x10,y10,x20,y20);"
    print "legend('1y','5y','10y','20y')"
    print "xlabel('Year');"
    print "ylabel('Percent of new edges');"
    print "saveas(gcf,'%s','png');" % (str(function).split(" ")[1])


definition = definition_C3
def_args = args_for_definition_C(10, 5000)

data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

for function in [percentage_of_new_edges_over_time, percentage_of_edge_sign_changes_over_time]:
    edge_proportion_over_time(data, definition, def_args, function, [1, 5, 10, 20])

