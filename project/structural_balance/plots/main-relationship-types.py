from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.structural_balance.definitions import definition_B, args_for_definition_B, NO_LINK
from project.structural_balance.plots.config import OUT_DIR
import csv

def write_relationship_types(data, definition, def_args, out_dir):
    for year in data.all_years:
        with open(out_dir + '%s.csv' % year, 'wb') as csvfile:
            out_file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            out_file.writerow(['Country1', 'Country2', 'Link type', 'Export/Import ratio'])
            for (A, B) in countries.country_pairs():
                link_type = definition(data, year, A, B, def_args)
                if link_type != NO_LINK:
                    out_file.writerow([A, B, link_type, data.export_import_ratio(A, B, year)])


data = ExportData()
data.load_export_data('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_B
def_args = args_for_definition_B(5)

write_relationship_types(data, definition, def_args, OUT_DIR.RELATIONSHIP_TYPES)
