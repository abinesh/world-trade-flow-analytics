from project.traids_vs_degree_plot.export_data.exportdata import ExportData
import re
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, WRITE_OUT_TO_DIR
from project.util import file_safe


def insert_into_slopes(map, exporter, importer, slope):
    if not exporter in map:
        map[exporter] = {}
    map[exporter][importer] = slope

slopes = {}

def read_slopes():
    f = open('../../dataset/r2-and-slopes-percent-sane.txt', 'r')
    for line in f:
        [exporter, importer_str, _, slope] = re.split(' ', line)
        importer = importer_str.replace(exporter + '-export-to-', '')
        insert_into_slopes(slopes, exporter, importer, float(slope))
        print line

read_slopes()

def slope_data(exporter, importer):
    return slopes[file_safe(exporter)][file_safe(importer)]


def trade_relationship_exists(exporter, importer):
    if file_safe(exporter) in slopes:
        if file_safe(importer) in slopes[file_safe(exporter)]:
            return True
    return False


def write_data_files_for_slope_vs_export_plots(data,root_dir, out_dir):
    f_countries_list = open(root_dir + '/' + out_dir + '/all-countries.txt', 'w')

    total_countries = 0
    for exporter in countries.countries:
        all_countries_file_name = out_dir + '/' + file_safe(exporter) + '.txt'
        world_file_name = out_dir + '/' + file_safe(exporter) + '-world.txt'

        f = open(root_dir + '/' + all_countries_file_name, 'w')
        f_world = open(root_dir + '/' + world_file_name, 'w')
        if not exporter == 'World':
            f_countries_list.write(file_safe(exporter) + ' ' + all_countries_file_name + ' ' + world_file_name + '\n')
            total_countries += 1
        for importer in countries.countries:
            if exporter == importer:
                continue
            if not trade_relationship_exists(exporter, importer):
                continue
            print exporter + ' ' + importer
            print str(slope_data(exporter, importer)) + ' ' + str(data.export_data(2000, exporter, importer))
            f.write(str(slope_data(exporter, importer)) + ' ' + str(data.export_data(2000, exporter, importer)) + '\n')
            if importer == 'World':
                f_world.write(
                    str(slope_data(exporter, importer)) + ' ' + str(data.export_data(2000, exporter, importer)) + '\n')

        f.close()
        f_world.close()
    f_countries_list.close()
    return total_countries

data = ExportData()
data.load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, ["Value00"],should_include_world=True)

total_countries = write_data_files_for_slope_vs_export_plots(data,'matlab', 'out/slope-vs-export-percent')
matlab_program_file = open('matlab/slope_vs_export_percent_gen.m', 'w')

matlab_program_file.write("clear" + '\n')
matlab_program_file.write("total = " + str(total_countries) + '\n')
matlab_program_file.write(
    "[country_names,all_countries,only_world]=textread('out/slope-vs-export-percent/all-countries.txt','%s %s %s' ,total)" + '\n')
matlab_program_file.write("" + '\n')
matlab_program_file.write("for i=1:total," + '\n')
matlab_program_file.write("    all_countries{i}" + '\n')
matlab_program_file.write("    all_data = load(all_countries{i})" + '\n')
matlab_program_file.write("    world_data = load(only_world{i})" + '\n')
matlab_program_file.write("" + '\n')
matlab_program_file.write("    if size(all_data)~=[0,0]" + '\n')
matlab_program_file.write("        all_slopes = all_data(:,1)" + '\n')
matlab_program_file.write("        all_exports = all_data(:,2)" + '\n')
matlab_program_file.write("" + '\n')
matlab_program_file.write("        world_slope = world_data(:,1)" + '\n')
matlab_program_file.write("        world_export = world_data(:,2)" + '\n')
matlab_program_file.write("" + '\n')
matlab_program_file.write("        plot(all_slopes,all_exports,'o',world_slope,world_export,'*r')" + '\n')
matlab_program_file.write("        xlabel('Linear regression slope')" + '\n')
matlab_program_file.write("        ylabel('Export in the year 2000')" + '\n')
matlab_program_file.write("        graph_file_name = sprintf('out/slope-vs-export-percent-graphs/%s',country_names{i})" + '\n')
matlab_program_file.write("        saveas(gcf,graph_file_name,'png')" + '\n')
matlab_program_file.write("    end" + '\n')
matlab_program_file.write("end" + '\n')

matlab_program_file.close()
