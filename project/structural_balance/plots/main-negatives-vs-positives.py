from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.structural_balance.definitions import definition_B, args_for_definition_B, NEGATIVE_LINK, POSITIVE_LINK
from project.util import file_safe

data = ExportData(1991, 2000)
data.load_export_data('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

def print_positives_and_negatives(data, definition, def_args, out_dir):
    in_files = open(out_dir + 'in_files.txt', 'w')
    for year in [1999, 2000]:
        file_name = 'y%s' % year
        data_file = open(out_dir + file_name + '.dat', 'w')
        in_files.write(out_dir + file_name + '\n')
        print year
        for A in countries.countries:
            positive = 0
            negative = 0
            for B in countries.countries:
                if A == B: continue
                link_type = definition(data, year, A, B, def_args)
                if link_type == NEGATIVE_LINK: negative += 1
                elif link_type == POSITIVE_LINK: positive += 1
            if positive == 0 and negative == 0:
                continue
            data_file.write("%s %d %d\n" % (file_safe(A), positive, negative))
        data_file.close()
    in_files.close()

print_positives_and_negatives(data, definition_B, args_for_definition_B(5), 'out/')
