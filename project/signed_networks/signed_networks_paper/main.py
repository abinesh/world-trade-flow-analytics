from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C1, args_for_definition_C, definition_C2, definition_D, args_for_definition_D, definition_A, definition_B, args_for_definition_A, args_for_definition_B
from project.signed_networks.signed_networks_paper.tables import table1, table2


def print_table(json):
    print json['Name']
    if json['Name'] == 'Table1':
        print json['Nodes']
        print json['Edges']
        print json['+ edges']
        print json['- edges']
        print json['Traids']
    elif json['Name'] == 'Table2':
        for t in ['T3', 'T1', 'T2', 'T0']:
            r = json[t]
            print "%s| %d \t| %.3g \t| %.3g \t| %.1f \t|" % (t, r['|Ti|'], r['p(Ti)'], r['p0(Ti)'], r['s(Ti)'])

data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

for table in [table1, table2]:
    print_table(table(data, 2000, definition_B, args_for_definition_B(5)))
    print_table(table(data, 2000, definition_C1, args_for_definition_C(5000, 1)))
    print_table(table(data, 2000, definition_C2, args_for_definition_C(10, 1)))
    print_table(table(data, 2000, definition_D, args_for_definition_D(90)))
