import csv
from numpy import polyfit, std
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


class ExportData:
    def __init__(self):
        self.years_map = {}
        self.missing_data_records_map = {}
        self.all_years = range(1963, 2001)
        for year in self.all_years:
            self.years_map[year] = self.__empty_data_for_a_year()
            self.missing_data_records_map[year] = {}
            print "Inited map for year %d " % year

    def __empty_data_for_a_year(self):
        list = []
        for index in countries.index_to_country_map.keys():
            list.append(Country(countries.index_to_country_map.get(index)))
        return list


    def __export_data_for_a_country(self, exporter, year):
        country_index = countries.country_to_index_map[exporter]
        return self.years_map[year][country_index]


    def export_data(self, year, exporter, importer, respect_missing_points=False):
        if respect_missing_points:
            if not self.__data_exists(year, exporter, importer):
                return None
        exporter_data_for_year = self.__export_data_for_a_country(exporter, year)
        return exporter_data_for_year.get_export_to_country(importer)


    def total_exports(self, exporter, year):
        return self.export_data(year, exporter, 'World')

    def expected_export_range(self, begin_year, end_year, exporter, importer):
        if not begin_year in self.all_years or not end_year in self.all_years:
            return None, None

        time_period = range(begin_year, end_year + 1)
        export_quantity_during_this_time_period = [self.export_data(year, exporter, importer) for year in time_period]
        (slope, intercept) = polyfit(time_period, export_quantity_during_this_time_period, 1)

        predicted_export_quantity = slope * (end_year + 1) + intercept
        standard_deviation = std(export_quantity_during_this_time_period)

        return predicted_export_quantity - standard_deviation, predicted_export_quantity + standard_deviation

    def load_export_data(self, file_path, year_columns=YEAR_COLUMNS, should_include_world=False):
        reader = csv.DictReader(open(file_path, 'rb'), skipinitialspace=True)

        for row in reader:
            importer = row.get('Importer')
            exporter = row.get('Exporter')
            if not should_include_world:
                if importer == 'World' or exporter == 'World':
                    continue
            if importer == exporter:
                continue
            if not is_valid_country(importer) or not is_valid_country(exporter):
                continue
            for column in year_columns:
                export_quantity = row.get(column)
                year = column_to_year(column)
                if export_quantity == 'NaN':
                    self.__record_missing_data(year, exporter, importer)
                    continue
                self.__export_data_for_a_country(exporter, year).set_export_to_country(importer, float(export_quantity))
                print "in " + str(year) + ", " + exporter + " exported " + export_quantity + " to " + importer

    def __record_missing_data(self, year, exporter, importer):
        m = self.missing_data_records_map[year]
        if exporter not in m:
            m[exporter] = {}
        m[exporter][importer] = 1

    def __data_exists(self, year, exporter, importer):
        m = self.missing_data_records_map[year]
        if exporter in m:
            if importer in m[exporter]:
                return False
        return True

