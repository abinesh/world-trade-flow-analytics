import csv
from numpy import polyfit, std
from project import countries
from project.config import YEAR_COLUMNS
from project.countries import is_valid_country, world_excluded_countries_list
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
    def __init__(self, start_year=1963, end_year=2000):
        self.years_map = {}
        self.missing_data_records_map = {}
        self.all_years = range(start_year, end_year + 1)
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


    def export_import_ratio(self, exporter, importer, year):
        num = self.export_data(year, exporter, importer)
        den = self.export_data(year, importer, exporter)
        val = -1
        if den != 0:
            val = num / den
        return val

    def export_data(self, year, exporter, importer, respect_missing_points=False):
        if respect_missing_points:
            if not self.__data_exists(year, exporter, importer):
                return None
        exporter_data_for_year = self.__export_data_for_a_country(exporter, year)
        return exporter_data_for_year.get_export_to_country(importer)

    def export_data_as_percentage(self, year, exporter, importer, return_none_if_data_point_is_nan=False):
        if return_none_if_data_point_is_nan:
            if not self.__data_exists(year, exporter, importer):
                return None
        print "%d,%s,%s" % (year, exporter, importer)
        exports_to_world = self.total_exports(exporter, year)
        if exports_to_world is None or exports_to_world == 0:
            return None
        return self.export_data(year, exporter, importer, return_none_if_data_point_is_nan) / exports_to_world


    def total_exports(self, exporter, year):
        return self.export_data(year, exporter, 'World')

    def bollinger_band_range(self, begin_year, end_year, exporter, importer):
        if not begin_year in self.all_years or not end_year in self.all_years:
            return None, None, None

        time_period = range(begin_year, end_year + 1)
        export_percentages = [self.export_data_as_percentage(year, exporter, importer, True) for year in time_period]
        if len(export_percentages) - export_percentages.count(None) < 3:
            return None, None, None

        filtered = [(y, q) for (y, q) in zip(time_period, export_percentages) if q is not None]
        filtered_time_period, filtered_export_percentages = zip(*filtered)

        (slope, intercept) = polyfit(filtered_time_period, filtered_export_percentages, 1)

        predicted_export_percentage = slope * (end_year + 1) + intercept
        standard_deviation = std(filtered_export_percentages)

        return slope, predicted_export_percentage - standard_deviation, predicted_export_percentage + standard_deviation

    def top_countries_by_export(self, year, k):
        countries_list = world_excluded_countries_list()
        all = [(self.total_exports(country, year), country) for country in countries_list]
        all.sort()
        size = len(all)
        topK = all[size - k:size]
        topK.reverse()
        return [c for v, c in topK]

    def load_export_data(self, file_path, year_columns=YEAR_COLUMNS, should_read_world_datapoints=False):
        reader = csv.DictReader(open(file_path, 'rb'), skipinitialspace=True)

        for row in reader:
            importer = row.get('Importer')
            exporter = row.get('Exporter')
            if not should_read_world_datapoints:
                if importer == 'World' or exporter == 'World':
                    continue
            if importer == exporter:
                continue
            if not is_valid_country(importer) or not is_valid_country(exporter):
                continue
            for column in year_columns:
                export_quantity = row.get(column)
                year = column_to_year(column)
                if not year in self.all_years:
                    continue
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

