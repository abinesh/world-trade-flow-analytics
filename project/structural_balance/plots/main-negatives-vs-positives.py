from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.structural_balance.definitions import definition_B, args_for_definition_B, NEGATIVE_LINK, POSITIVE_LINK
from project.util import file_safe

data = ExportData()
data.load_export_data('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

def print_positives_and_negatives(data, definition, def_args, out_dir):
    in_files = open(out_dir + 'in_files.txt', 'w')
    for year in data.all_years:
        file_name = 'y%s' % year
        data_file = open(out_dir + file_name + '.dat', 'w')
        in_files.write(file_name + '\n')
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


'''
clear
close(gcf)
in_files_size = -1
in_files=textread('in_files.txt','%s',in_files_size)
[in_files_size,unused]=size(in_files)
for i=1:in_files_size,
    [countries,positives,negatives]= textread(strcat(in_files{i},'.dat'),'%s %d %d')
    end_point = max(positives)
    if end_point < max(negatives)
        end_point = max(negatives)
    end
    loglog([positives;end_point],[negatives;end_point],'o')
    text([positives;end_point],[negatives;end_point],[countries;'end'],'FontSize',7)
    xlabel('Number of positive links')
    ylabel('Number of negative links')
    graph_file_name = sprintf('pngs/positives-vs-negatives-%s.png',in_files{i})
    saveas(gcf,graph_file_name,'png')
end
'''
