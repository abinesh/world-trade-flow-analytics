import re
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE, WRITE_OUT_TO_DIR
from project.traids_vs_degree_plot.export_data.exportdata import  load_export_data, export_data
from project.util import file_safe


def insert_into_slopes(map, exporter, importer, slope):
    if not exporter in map:
        map[exporter] = {}
    map[exporter][importer] = slope

slopes = {}

def read_slopes():
    f = open('../../dataset/r2-and-slopes-sane.txt', 'r')
    for line in f:
        [exporter, importer_str, _, slope] = re.split(' ', line)
        importer = importer_str.replace(exporter + '-export-to-', '')
        insert_into_slopes(slopes, exporter, importer, float(slope))
        print line

read_slopes()
load_export_data(WORLD_TRADE_FLOW_DATA_FILE,["Value00"])

def slope_data(exporter, importer):
    return slopes[file_safe(exporter)][file_safe(importer)]


def trade_relationship_exists(exporter, importer):
    if file_safe(exporter) in slopes:
        if file_safe(importer) in slopes[file_safe(exporter)]:
            return True
    return False


def write_data_files_for_slope_vs_export_plots(out_dir):
    f_countries_list = open(out_dir + '/all-countries.txt', 'w')

    for exporter in countries.countries:
        f = open(out_dir + '/' + file_safe(exporter) + '.txt', 'w')
        f_world = open(out_dir + '/' + file_safe(exporter) + '-world.txt', 'w')
        f_countries_list.write(file_safe(exporter) + '\n')
        for importer in countries.countries:
            if exporter == importer:
                continue
            if not trade_relationship_exists(exporter, importer):
                continue
            print exporter + ' ' + importer
            print str(slope_data(exporter, importer)) + ' ' + str(export_data(2000, exporter, importer))
            f.write(str(slope_data(exporter, importer)) + ' ' + str(export_data(2000, exporter, importer)) + '\n')
            if importer == 'World':
                f_world.write(
                    str(slope_data(exporter, importer)) + ' ' + str(export_data(2000, exporter, importer)) + '\n')

        f.close()
        f_world.close()
    f_countries_list.close()

write_data_files_for_slope_vs_export_plots('matlab/out/slope-vs-export')