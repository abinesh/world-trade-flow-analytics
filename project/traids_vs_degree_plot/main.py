from project.config import  WORLD_TRADE_FLOW_DATA_FILE
from project.traids_vs_degree_plot import config
from project.traids_vs_degree_plot.export_data import  strongties
from project.traids_vs_degree_plot.csv_writer.csv_writer import csv_write
from project.traids_vs_degree_plot.export_data.exportdata import all_years, load_export_data


def write_out_graph_data_for_traids_vs_degree_plot():
    for year in all_years:
        matrix_for_a_year = strongties.matrix_for_year_method_B(year, config.STRONG_TIES_LOWER_BOUND,
            config.STRONG_TIES_UPPER_BOUND)
        csv_write(config.graph_data_file_name(year), strongties.graph_data(matrix_for_a_year))

load_export_data(WORLD_TRADE_FLOW_DATA_FILE)
write_out_graph_data_for_traids_vs_degree_plot()




