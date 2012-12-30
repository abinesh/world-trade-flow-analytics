import json
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.structural_balance.definitions import definition_B, args_for_definition_B, NEGATIVE_LINK, POSITIVE_LINK
from project.util import file_safe


def positives_and_negatives_data_matlab(data, definition, def_args, out_dir):
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


def positives_and_negatives_data_d3(data, definition, def_args, out_dir):
#    countries_list = ["USA","UK","Turkey"]
    countries_list = countries.countries

    class NationData:
        def __init__(self, country_name):
            self.name = country_name
            self.region = country_name
            self.positive_links_count = []
            self.negative_links_count = []
            self.export_quantity = []

        def add_data(self, year, p, n, ex):
            self.positive_links_count.append([year, p])
            self.negative_links_count.append([year, n])
            self.export_quantity.append([year, ex])

    all_nations_dict = []

    json_file = open(out_dir + 'nations_gen.json', 'w')
    for A in countries_list:
        nation = NationData(A)
        for year in data.all_years:
            positive = 0
            negative = 0
            for B in countries_list:
                if A == B: continue
                link_type = definition(data, year, A, B, def_args)
                if link_type == NEGATIVE_LINK: negative += 1
                elif link_type == POSITIVE_LINK: positive += 1
            nation.add_data(year, positive, negative, data.total_exports(A, year))
        all_nations_dict.append(nation.__dict__)

    json_file.write(json.dumps(all_nations_dict))
    json_file.close()

data = ExportData()
data.load_export_data('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

positives_and_negatives_data_d3(data, definition_B, args_for_definition_B(5), 'out/')
#positives_and_negatives_data_matlab(data, definition_B, args_for_definition_B(5), 'out/')


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
