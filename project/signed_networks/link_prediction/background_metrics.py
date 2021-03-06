from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C, POSITIVE_LINK, NEGATIVE_LINK
from project.signed_networks.link_prediction.link import percentage_of_new_edges_over_time, percentage_of_edge_sign_changes_over_time, hops_count_before_edge_vs_count, inf_scale_adjust, count_of_bridge_configs, is_new_edge, did_sign_change
from project.util import array_as_matlab_row


def edge_proportion_over_time(data, definition, def_args, function, look_back_durations):
    for look_back_duration in look_back_durations:
        x_axis = data.all_years[look_back_duration:]
        print "x%d=%s;" % (look_back_duration, str(x_axis).replace(",", ""))
        print "y%d=%s;" % (look_back_duration, str(
            [function(data, definition, def_args, year, look_back_duration) for year in x_axis]).replace(",", ""))
    print "plot(x1,y1,x5,y5,x10,y10,x20,y20);"
    print "legend('1y','5y','10y','20y')"
    print "xlabel('Year');"
    function_name = str(function).split(" ")[1]
    print "ylabel('%s');" % function_name.replace("_", " ")
    print "saveas(gcf,'%s','png');" % function_name


def number_of_hops_before_forming_edge(data, definition, def_args, year, look_back_durations):
    index = 0
    (adjusted_hops, inf_x_axis_position) = inf_scale_adjust(
        [hops_count_before_edge_vs_count(data, definition, def_args, year, look_back_duration) for look_back_duration in
         look_back_durations])
    for hop in adjusted_hops:
        print "x%d=%s" % (look_back_durations[index], str([x for (x, _) in hop]).replace(",", ""))
        print "y%d=%s" % (look_back_durations[index], str([y for (_, y) in hop]).replace(",", ""))
        index += 1

    print "plot(x1,y1,x5,y5,x10,y10,x20,y20);"
    print "legend('1y','5y','10y','20y')"
    print "xlabel('Number of hops');"
    print "ylabel('Count');"
    print "saveas(gcf,'Number-of-hops-before-link-%d','png');" % year


def bridge_type_before_(data, definition, def_args, year, look_back_durations, edge_selection):
    print "y1=[%s];" % (';'.join([array_as_matlab_row(
        [count_of_bridge_configs(data, definition, def_args, year, look_back_duration, bridge_type, edge_selection,
                                 POSITIVE_LINK) for look_back_duration in look_back_durations]) for bridge_type in
                                  ["2+", "+-", "2-"]]))
    print "y2=[%s];" % (';'.join([array_as_matlab_row(
        [count_of_bridge_configs(data, definition, def_args, year, look_back_duration, bridge_type, edge_selection,
                                 NEGATIVE_LINK) for look_back_duration in look_back_durations]) for bridge_type in
                                  ["2+", "+-", "2-"]]))
    print "y=[y1;y2];"
    print "bar(y,'grouped');"
    print "legend('1y','5y','10y','20y','Location','Best');"
    print "set(gca,'XTickLabel',{'2++','+-+','2-+','2+-','+--','2--'});"
    function_name = str(edge_selection).split(" ")[1]
    print "saveas(gcf,'Bridge-type-%s-%d','png');" % (function_name, year)
    print "set(gca, 'YScale', 'log');"
    print "saveas(gcf,'log-Bridge-type-%s-%d','png');" % (function_name, year)


definition = definition_C3
def_args = args_for_definition_C(10, 5000)

data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

# for function in [percentage_of_new_edges_over_time, percentage_of_edge_sign_changes_over_time]:
#     edge_proportion_over_time(data, definition, def_args, function, [1, 5, 10, 20])
# for year in range(1983, 2001):
#     number_of_hops_before_forming_edge(data, definition, def_args, year, [1, 5, 10, 20])
for edge_selection in [is_new_edge, did_sign_change]:
    for year in range(1983, 2001):
        bridge_type_before_(data, definition, def_args, year, [1, 5, 10, 20], edge_selection)
