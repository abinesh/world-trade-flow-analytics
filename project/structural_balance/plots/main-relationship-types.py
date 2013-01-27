from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.export_data.strongties import get_relationship_matrix, __matrix_cube, number_of_traids
from project.structural_balance.definitions import definition_B, args_for_definition_B, NO_LINK, POSITIVE_LINK
from project.structural_balance.plots.config import OUT_DIR
import csv

def write_relationship_types(data, definition, def_args, out_dir):
    for year in data.all_years:
        with open(out_dir + '%s.csv' % year, 'wb') as csvfile:
            out_file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            out_file.writerow(['Country1', 'Country2', 'Link type', 'Export/Import ratio'])
            for (A, B) in countries.country_pairs(data.countries()):
                link_type = definition(data, year, A, B, def_args)
                if link_type != NO_LINK:
                    out_file.writerow([A, B, link_type, data.export_import_ratio(A, B, year)])


def write_number_of_positive_traids(data, definition, def_args, out_dir):
    def relationship_def(data, year, A, B, def_args1):
        return definition(data, year, A, B, def_args) == POSITIVE_LINK

    all_years_data = {}
    years = data.all_years
    countries_list = data.countries()

    for year in years:
        single_year_data = {}
        with open(out_dir + '%s.csv' % year, 'wb') as csvfile:
            out_file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            out_file.writerow(['Country', 'Number of positive traids'])
            relationship_matrix = get_relationship_matrix(data, year, relationship_def, {})
            relationship_matrix_cube = __matrix_cube(relationship_matrix)
            for C in countries_list:
                number_of_positive_traids = number_of_traids(relationship_matrix_cube, C)
                out_file.writerow([C, number_of_positive_traids])
                single_year_data[C] = number_of_positive_traids
        all_years_data[year] = single_year_data

    with open(out_dir + 'all-years.csv', 'wb') as csvfile:
        out_file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        header = ['*']
        for C in countries_list:
            header.append(C)
        out_file.writerow(header)
        for year in years:
            row = [year]
            for C in countries_list:
                row.append(all_years_data[year][C])
            out_file.writerow(row)


data = ExportData()
data.load_export_data('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_B
subtypes_out = open(OUT_DIR.RELATIONSHIP_TYPES + 'subtypes.txt', 'w')
def_args = args_for_definition_B(5, subtypes_out)
write_relationship_types(data, definition, def_args, OUT_DIR.RELATIONSHIP_TYPES)
subtypes_out.close()
#write_number_of_positive_traids(data, definition, def_args, OUT_DIR.NUMBER_OF_POSITIVE_TRAIDS)
