import csv
from project import countries
from project.config import YEAR_COLUMNS
from project.countries import is_valid_country
from project.util import column_to_year

class Country:
    def __init__(self, name):
        self.name = name
        self.list = []
        for k in countries.index_to_country_map.keys():
            name = countries.index_to_country_map.get(k)
            self.list.append((name, 0))

    def set_export_to_country(self, country, quantity):
        self.list[countries.country_to_index_map[country]] = (country, quantity)

    def get_export_to_country(self, country):
        return self.list[countries.country_to_index_map[country]][1]


def empty_data_for_a_year():
    list = []
    for index in countries.index_to_country_map.keys():
        list.append(Country(countries.index_to_country_map.get(index)))
    return list

years_map = {}
all_years = range(1963, 2001)
for year in all_years:
    years_map[year] = empty_data_for_a_year()
    print year


def export_data_for_a_country(exporter, year):
    country_index = countries.country_to_index_map[exporter]
    return years_map[year][country_index]


def export_data(year, exporter, importer):
    exporter_data_for_year = export_data_for_a_country(exporter, year)
    return exporter_data_for_year.get_export_to_country(importer)


def load_export_data(file_path):
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
            export_data_for_a_country(exporter, year).set_export_to_country(importer, float(export_quantity))
            print "in " + str(year) + ", " + exporter + " exported " + export_quantity + " to " + importer


