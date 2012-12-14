from project.config import  WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.traids_vs_degree_plot import config
from project.traids_vs_degree_plot.export_data import  strongties
from project.traids_vs_degree_plot.csv_writer.csv_writer import csv_write
from project.traids_vs_degree_plot.export_data.exportdata import ExportData


def write_out_graph_data_for_traids_vs_degree_plot(data):
    for year in data.all_years:
        matrix_for_a_year = strongties.matrix_for_year_method_B(data,year, config.STRONG_TIES_LOWER_BOUND,
            config.STRONG_TIES_UPPER_BOUND)
        csv_write(config.graph_data_file_name(year), strongties.graph_data(matrix_for_a_year))

data = ExportData()
data.load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL)
write_out_graph_data_for_traids_vs_degree_plot(data)




