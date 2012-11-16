import re
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE
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
load_export_data(WORLD_TRADE_FLOW_DATA_FILE)

def slope_data(exporter, importer):
    return slopes[file_safe(exporter)][file_safe(importer)]


def trade_relationship_exists(exporter, importer):
    if file_safe(exporter) in slopes:
        if file_safe(importer) in slopes[file_safe(exporter)]:
            return True
    return False

for exporter in countries.countries:
    for importer in countries.countries:
        if exporter == importer:
            continue
        if not trade_relationship_exists(exporter, importer):
            continue
        print exporter + ' ' + importer
        print str(slope_data(exporter, importer)) + ' ' + str(export_data(2000, exporter, importer))
