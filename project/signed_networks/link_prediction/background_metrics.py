from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.link_prediction.link import percentage_of_new_links


def new_edge_over_time(data, definition, def_args, look_back_duration):
    x_axis = data.all_years[look_back_duration:]
    print "x=%s;" % str(x_axis).replace(",", "")
    print "y=%s;" % str(
        [percentage_of_new_links(data, definition, def_args, year, look_back_duration) for year in x_axis]).replace(",",
                                                                                                                    "")
    print "plot(x,y);"
    print "xlabel('Year');"
    print "ylabel('Percent of new edges');"
    print "saveas(gcf,'percent-of-new-edges-over-time-%d-years','png');" % look_back_duration


definition = definition_C3
def_args = args_for_definition_C(10, 5000)

data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)
new_edge_over_time(data, definition, def_args, 1)
new_edge_over_time(data, definition, def_args, 5)
new_edge_over_time(data, definition, def_args, 10)
new_edge_over_time(data, definition, def_args, 20)

