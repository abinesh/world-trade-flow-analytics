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
            self.list.append((name, -1))

    def set_export_to_country(self, country, quantity):
        self.list[countries.country_to_index_map[country]] = (country, quantity)

    def get_export_to_country(self, country):
        return self.list[countries.country_to_index_map[country]][1]


class ExportData:
    def __init__(self, start_year=1963, end_year=2000):
        self.cache = {}
        self.years_map = {}
        self.nan_records_map = {}
        self.all_years = range(start_year, end_year + 1)
        for year in self.all_years:
            self.years_map[year] = self.__empty_data_for_a_year()
            self.nan_records_map[year] = {}
            print "Inited map for year %d " % year
        self.inflation_data = {
            '1963': 4.5,
            '1964': 4.4,
            '1965': 6.3,
            '1966': 17.2,
            '1967': 2.5,
            '1968': 13.7,
            '1969': 0.8,
            '1970': 7.6,
            '1971': 4.5,
            '1972': 14.5,
            '1973': 7.5,
            '1974': 9.5,
            '1975': 7.4,
            '1976': 5.3,
            '1977': 4.5,
            '1978': 3.7,
            '1979': 14.9,
            '1980': 6.7,
            '1981': 18.4,
            '1982': 9.2,
            '1983': 3.7,
            '1984': 2.9,
            '1985': 14.7,
            '1986': 1.3,
            '1987': 6.2,
            '1988': 14.5,
            '1989': 3.5,
            '1990': 2.7,
            '1991': 4.8,
            '1992': 16.5,
            '1993': 7.2,
            '1994': 9.1,
            '1995': 4.1,
            '1996': 13.1,
            '1997': 12.2,
            '1998': 3.5,
            '1999': 5.7,
            '2000': 16.8,
        }

    def __empty_data_for_a_year(self):
        list = []
        for index in countries.index_to_country_map.keys():
            list.append(Country(countries.index_to_country_map.get(index)))
        return list


    def __export_data_for_a_country(self, exporter, year):
        country_index = countries.country_to_index_map[exporter]
        return self.years_map[year][country_index]

    def cache_key(self, func, *args):
        return "%s,%s" % (func.__name__, ",".join([str(a) for a in args]))

    def sorted_list_of_export_percentages(self, exporter, year):
        cache_key = self.cache_key(self.sorted_list_of_export_percentages, exporter, year)
        if cache_key in self.cache:
            return self.cache[cache_key]
        result = [(c, self.export_data_as_percentage(year, exporter, c)) for c in
                  countries.world_excluded_countries_list() if
                  self.export_data_as_percentage(year, exporter, c) != 0]
        ret_val = [(a, 100 * b) for (a, b) in
                   sorted(result, key=lambda country: 0 if country[1] is None else -country[1])
                   if b is not None]
        self.cache[cache_key] = ret_val
        return ret_val

    def top_T_percent_exports(self, exporter, year, T):
        cache_key = self.cache_key(self.sorted_list_of_export_percentages, exporter, year)
        if cache_key in self.cache:
            return self.cache[cache_key]
        (total, ret_val, tie_percent) = (0, [], -1)
        for (C, percent) in self.sorted_list_of_export_percentages(exporter, year):
            total += percent
            if total > T and tie_percent == -1:
                tie_percent = percent
            elif total > T and percent < tie_percent:
                break
            ret_val.append(C)

        self.cache[cache_key] = ret_val
        return ret_val


    def export_import_ratio(self, exporter, importer, year):
        num = self.export_data(year, exporter, importer)
        den = self.export_data(year, importer, exporter)
        val = -1
        if den != 0:
            val = num / den
        return val

    def export_data(self, year, exporter, importer,
                    return_none_if_data_point_is_nan=False,
                    return_this_for_missing_datapoint=0):
        if return_none_if_data_point_is_nan:
            if not self.__data_exists(year, exporter, importer):
                return None
        exporter_data_for_year = self.__export_data_for_a_country(exporter, year)
        retval = exporter_data_for_year.get_export_to_country(importer)
        if retval == -1: return return_this_for_missing_datapoint
        return retval

    def _adjust_inflation(self, value, year):
        current_year = year
        beginning = 1963
        while current_year >= beginning:
            value = (100 * value) / (100 + self.inflation_data['%s' % current_year])
            current_year -= 1
        return value

    def export_data_inflation_adjusted(self, year, exporter, importer,
                                       return_none_if_data_point_is_nan=False,
                                       return_this_for_missing_datapoint=0):
        actual_export_data = self.export_data(year, exporter, importer,
            return_none_if_data_point_is_nan,
            return_this_for_missing_datapoint)
        if actual_export_data is None: return None
        if actual_export_data == -1: return return_this_for_missing_datapoint
        return self._adjust_inflation(actual_export_data, year)

    def export_data_as_percentage(self, year, exporter, importer,
                                  return_none_if_data_point_is_nan=False,
                                  return_this_for_missing_datapoint=0):
        if return_none_if_data_point_is_nan:
            if not self.__data_exists(year, exporter, importer):
                return None
        exports_to_world = self.total_exports(exporter, year)
        if exports_to_world is None or exports_to_world == 0:
            return None
        val = self.export_data(year, exporter, importer, return_none_if_data_point_is_nan,
            return_this_for_missing_datapoint)
        if val == -1: return return_this_for_missing_datapoint
        return val / exports_to_world

    def total_exports_from_C1_to_C2(self, C1, C2):
        cache_key = self.cache_key(self.total_exports_from_C1_to_C2, C1, C2)
        if cache_key in self.cache:
            return self.cache[cache_key]

        total = 0
        for year in self.all_years:
            v = self.export_data(year, C1, C2)
            if v is not None: total += v

        self.cache[cache_key] = total
        return total

    def total_non_nan_points_from_C1_to_C2(self, C1, C2):
        cache_key = self.cache_key(self.total_non_nan_points_from_C1_to_C2, C1, C2)
        if cache_key in self.cache:
            return self.cache[cache_key]

        retval = 0
        for year in self.all_years:
            v = self.export_data(year, C1, C2,
                return_none_if_data_point_is_nan=True,
                return_this_for_missing_datapoint=-1)
            if v == -1:
                retval = -1
                break
            if v is not None: retval += 1

        self.cache[cache_key] = retval
        return retval

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
                    self.__record_nan_data(year, exporter, importer)
                    continue
                self.__export_data_for_a_country(exporter, year).set_export_to_country(importer, float(export_quantity))
                print "in " + str(year) + ", " + exporter + " exported " + export_quantity + " to " + importer

    def __record_nan_data(self, year, exporter, importer):
        m = self.nan_records_map[year]
        self.__export_data_for_a_country(exporter, year).set_export_to_country(importer, 0)
        if exporter not in m:
            m[exporter] = {}
        m[exporter][importer] = 1

    def __data_exists(self, year, exporter, importer):
        m = self.nan_records_map[year]
        if exporter in m:
            if importer in m[exporter]:
                return False
        return True

    def first_positive_year(self, C1, C2):
        cache_key = self.cache_key(self.first_positive_year, C1, C2)
        if cache_key in self.cache:
            return self.cache[cache_key]

        current_year = self.all_years[0]
        end_year = self.all_years[len(self.all_years) - 1]
        retval = None
        while current_year <= end_year:
            if self.export_data(current_year, C1, C2) is None or self.export_data(current_year, C1, C2) == 0:
                current_year += 1
            else:
                retval = current_year
                break
        if retval is None: retval = end_year + 1
        self.cache[cache_key] = retval
        return retval
