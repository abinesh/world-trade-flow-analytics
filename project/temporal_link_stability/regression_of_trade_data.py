import csv
import os
from project import countries
from project.config import YEAR_COLUMNS, WORLD_TRADE_FLOW_DATA_FILE
from project.countries import is_valid_country
from project.util import column_to_year


def file_safe(country):
    return country.replace(',', '_').replace('.', '_').replace(' ', '_')


def write_intermediate_data_files_for_matlab_plots(input_file, f1, f2, f3):
    i = 0
    reader = csv.DictReader(open(input_file, 'rb'), skipinitialspace=True)
    out1 = open(f1, 'w')
    out2 = open(f2, 'w')
    out3 = open(f3, 'w')
    for row in reader:
        importer = row.get('Importer')
        exporter = row.get('Exporter')
        if importer == exporter:
            continue
        if not is_valid_country(importer) or not is_valid_country(exporter):
            continue
        rootdir = 'matlab/'
        subdir = 'in/wtf/' + file_safe(exporter) + '/'
        filepath = subdir + 'exports-to-' + file_safe(importer) + '.txt'

        if not os.path.exists(rootdir + subdir):
            os.makedirs(rootdir + subdir)
        with open(rootdir + filepath, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            for column in YEAR_COLUMNS:
                export_quantity = row.get(column)
                if(export_quantity == 'NaN'):
                    continue
                year = column_to_year(column)
                writer.writerow([year, export_quantity])

        out1.write(filepath + "\n")
        out2.write(
            "out/wtf/" + file_safe(exporter) + "/" + file_safe(exporter) + "-export-to-" + file_safe(importer) + "\n")
        print i
        i += 1

    for c in countries.countries:
        out3.write("mkdir('out/wtf/" + file_safe(c) + "')\n")

    out3.write("clear\n")
    out3.write("total = " + str(i) + "\n")
    out3.write("inputfile123=textread('input-files.txt','%s',total)\n")
    out3.write("outputfile123=textread('output-files.txt','%s',total)\n")
    out3.write("\n")
    out3.write("for i=1:total,\n")
    out3.write("    data = load(inputfile123{i})\n")
    out3.write("    datasize = size(data)\n")
    out3.write("    isemptyfile = datasize(1) == 0\n")
    out3.write("    if isemptyfile\n")
    out3.write("        data = [0 0]\n")
    out3.write("    end\n")
    out3.write("    x = data(:,1)\n")
    out3.write("    y = data(:,2)\n")
    out3.write("    ylinearfit = polyval(polyfit(x,y,1),x)\n")
    out3.write("    yquadfit = polyval(polyfit(x,y,2),x)\n")
    out3.write("    plot(x,y,'k-s',x,ylinearfit,x,yquadfit)\n")
    out3.write("    if isemptyfile\n")
    out3.write("        xlabel('No data')\n")
    out3.write("        ylabel('No data')\n")
    out3.write("    else\n")
    out3.write("        xlabel('Year')\n")
    out3.write("        ylabel('Export Quantity')\n")
    out3.write("    end\n")
    out3.write("    saveas(gcf,outputfile123{i},'png')\n")
    out3.write("    i\n")
    out3.write("end\n")

write_intermediate_data_files_for_matlab_plots(WORLD_TRADE_FLOW_DATA_FILE, 'matlab/input-files.txt', 'matlab/output-files.txt', 'matlab/generateplotsloop.m')
