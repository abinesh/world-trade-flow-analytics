import csv
from project.config import YEAR_COLUMNS, WORLD_TRADE_FLOW_DATA_FILE
from project.traids_vs_degree_plot import config
from project.traids_vs_degree_plot.export_data import exportdata, strongties
from project.countries import is_valid_country
from project.traids_vs_degree_plot.csv_writer.csv_writer import csv_write
from project.traids_vs_degree_plot.export_data.exportdata import all_years
from project.util import column_to_year


def read_file(file_path):
    reader = csv.DictReader(open(file_path, 'rb'), skipinitialspace=True)

    for row in reader:
        importer = row.get('Importer')
        exporter = row.get('Exporter')
        if (importer == 'World' or exporter == 'World') or (importer == exporter):
            continue
        if not is_valid_country(importer) or not is_valid_country(exporter):
            continue
        for column in YEAR_COLUMNS:
            export_quantity = row.get(column)
            if(export_quantity == 'NaN'):
                continue
            year = column_to_year(column)
            exportdata.export_data_for_a_country(exporter, year).set_export_to_country(importer, float(export_quantity))
            print "in " + str(year) + ", " + exporter + " exported " + export_quantity + " to " + importer


def write_out_graph_data_for_traids_vs_degree_plot():
    for year in all_years:
        matrix_for_a_year = strongties.matrix_for_year_method_B(year, config.STRONG_TIES_LOWER_BOUND,
            config.STRONG_TIES_UPPER_BOUND)
        csv_write(config.graph_data_file_name(year), strongties.graph_data(matrix_for_a_year))

read_file(WORLD_TRADE_FLOW_DATA_FILE)
write_out_graph_data_for_traids_vs_degree_plot()




