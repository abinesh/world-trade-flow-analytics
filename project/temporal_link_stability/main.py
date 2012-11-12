import csv
import os
from project.config import YEAR_COLUMNS, WORLD_TRADE_FLOW_DATA_FILE
from project.countries import is_valid_country
from project.util import column_to_year


def file_safe(country):
    return country.replace(',', '_').replace('.', '_').replace(' ', '_')


def read_file(file_path):
    reader = csv.DictReader(open(file_path, 'rb'), skipinitialspace=True)

    for row in reader:
        importer = row.get('Importer')
        exporter = row.get('Exporter')
        if (importer == 'World' or exporter == 'World') or (importer == exporter) or exporter != 'USA':
            continue
        if not is_valid_country(importer) or not is_valid_country(exporter):
            continue
        rootdir = 'matlab/'
        subdir = 'in/wtf/' + file_safe(exporter) + '/'
        filepath = subdir + 'exports-to-' + file_safe(importer) + '.dat'

        if not os.path.exists(rootdir+subdir):
            os.makedirs(rootdir+subdir)
        with open(rootdir + filepath, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            for column in YEAR_COLUMNS:
                export_quantity = row.get(column)
                if(export_quantity == 'NaN'):
                    continue
                year = column_to_year(column)
                writer.writerow([year, export_quantity])

        print "clear"
        print "data = load('" + filepath + "')"
        print "x = data(:,1)"
        print "y = data(:,2)"
        print "yfit = polyval(polyfit(x,y,1),x)"
        print "plot(x,y,'o',x,yfit)"
        print "xlabel('Year')"
        print "ylabel('Export Quantity')"
        print "saveas(gcf,'out/wtf/" + file_safe(exporter) + "-export-to-" + file_safe(importer) + "','jpg')"


read_file(WORLD_TRADE_FLOW_DATA_FILE)
