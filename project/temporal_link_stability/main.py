import csv
import os
from project.config import YEAR_COLUMNS, WORLD_TRADE_FLOW_DATA_FILE
from project.countries import is_valid_country
from project.util import column_to_year


def file_safe(country):
    return country.replace(',', '_').replace('.', '_').replace(' ', '_')


def read_file(input_file, output_file):
    i=0
    reader = csv.DictReader(open(input_file, 'rb'), skipinitialspace=True)
    out = open(output_file, 'w')
    for row in reader:
        importer = row.get('Importer')
        exporter = row.get('Exporter')
        if (importer == 'World' or exporter == 'World') or (importer == exporter):
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

        out.write("clear\n")
        out.write("data = load('" + filepath + "')\n")
        out.write("x = data(:,1)\n")
        out.write("y = data(:,2)\n")
        out.write("ylinearfit = polyval(polyfit(x,y,1),x)\n")
        out.write("yquadfit = polyval(polyfit(x,y,2),x)\n")
        out.write("plot(x,y,'k-s',x,ylinearfit,x,yquadfit)\n")
        out.write("xlabel('Year')\n")
        out.write("ylabel('Export Quantity')\n")
        out.write("saveas(gcf,'out/wtf/" + file_safe(exporter) + "-export-to-" + file_safe(importer) + "','jpg')\n")
        print i
        i+=1


read_file(WORLD_TRADE_FLOW_DATA_FILE, 'matlab/generateplots.m')
