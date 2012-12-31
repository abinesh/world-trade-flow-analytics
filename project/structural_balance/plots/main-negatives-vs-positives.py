import json
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.structural_balance.definitions import definition_B, args_for_definition_B, NEGATIVE_LINK, POSITIVE_LINK
from project.structural_balance.plots.config import OUT_DIR

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
data.load_export_data('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

positives_and_negatives_data_d3(data, definition_B, args_for_definition_B(5), OUT_DIR.POSITIVES_AND_NEGATIVES)