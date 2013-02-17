import csv
from numpy import polyfit, std
from project import countries
from project.config import YEAR_COLUMNS
from project.countries import is_valid_country
from project.util import column_to_year, memoize

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
        self.years_map = {}
        self.nan_records_map = {}
        self.all_years = range(start_year, end_year + 1)
        self.all_countries = {}
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

    @memoize
    def countries(self):
        retval = self.all_countries.keys()
        retval.remove('World')
        return retval


    def __export_data_for_a_country(self, exporter, year):
        country_index = countries.country_to_index_map[exporter]
        return self.years_map[year][country_index]

    #    this method excludes (A,B) missing and (A,B)=Nan
    @memoize
    def sorted_list_of_export_percentages(self, exporter, year):
        list = [(B, self.export_data_as_percentage(year, exporter, B))
                for B in self.countries()
                if self.export_data_as_percentage(year, exporter, B) != 0]
        return [(a, 100 * b) for (a, b) in
                sorted(list, key=lambda country: 0 if country[1] is None else -country[1])
                if b is not None]

        #    this method includes (A,B) missing and (A,B)=Nan

    @memoize
    def countries_sorted_by_export_percentages(self, exporter, year, countries=None):
        if countries is None: countries = self.countries()
        list = [(B, 100 * self.export_data_as_percentage(year, exporter, B, False))
                for B in countries
                if self.export_data_as_percentage(year, exporter, B, False) is not None and exporter != B]
        return sorted(list, key=lambda country: 0 if country[1] is None else -country[1])

    def _pick_top_T(self, list, T):
        total, i = 0, 0
        while i < len(list) and (total <= T or (i - 1 >= 0 and list[i - 1][1] == list[i][1])):
            total += list[i][1]
            i += 1
        return [a for (a, _) in list[:i]]

    @memoize
    def top_T_percent_exports(self, exporter, year, T):
        return self._pick_top_T(self.sorted_list_of_export_percentages(exporter, year), T)

    def _calculate_export_percentile(self, B, list):
        if len(list) == 0: return 100.0
        retval = 0
        previous_percentage = -1
        total = 0
        for (C, percent) in list:
            if percent != previous_percentage: retval = total
            total += percent
            if C == B: return retval
            previous_percentage = percent
        return 100

    #this method does not work properly yet for (A,B) missing. It should return 100.0
    @memoize
    def export_data_as_percentile(self, year, A, B):
        if not self._trade_exists(year, A, B): return 100.0
        return self._calculate_export_percentile(B, self.sorted_list_of_export_percentages(A, year))


    def export_import_ratio(self, exporter, importer, year):
        num = self.export_data(year, exporter, importer)
        den = self.export_data(year, importer, exporter)
        val = -1
        if den != 0:
            val = num / den
        return val

    #    export from A->B can be missing, Nan or non-zero
    #    Default value when A->B is missing: -1
    #    Default value when A->B is Nan: 0
    def export_data(self, year, exporter, importer,
                    return_none_if_data_point_is_nan=False,
                    return_this_for_missing_datapoint=0):
        if return_none_if_data_point_is_nan and self._is_nan(year, exporter, importer):
            return None
        exporter_data_for_year = self.__export_data_for_a_country(exporter, year)
        retval = exporter_data_for_year.get_export_to_country(importer)
        assert retval is not None
        if retval == -1: return return_this_for_missing_datapoint
        return retval

    def export_data_as_percentage(self, year, exporter, importer,
                                  return_none_if_data_point_is_nan=False,
                                  return_this_for_missing_datapoint=0):
        if return_none_if_data_point_is_nan and self._is_nan(year, exporter, importer):
            return None
        exports_to_world = self.total_exports(exporter, year)
        if exports_to_world is None or exports_to_world == 0:
            return None
        val = self.export_data(year, exporter, importer, return_none_if_data_point_is_nan,
            return_this_for_missing_datapoint)
        if val == -1: return return_this_for_missing_datapoint
        return val / exports_to_world

    @memoize
    def total_exports_from_C1_to_C2(self, C1, C2):
        total = 0
        for year in self.all_years:
            v = self.export_data(year, C1, C2)
            if v is not None: total += v
        return total

    @memoize
    def total_non_nan_points_from_C1_to_C2(self, C1, C2):
        retval = 0
        for year in self.all_years:
            v = self.export_data(year, C1, C2,
                return_none_if_data_point_is_nan=True,
                return_this_for_missing_datapoint=-1)
            if v == -1:
                retval = 0
                break
            if v is not None: retval += 1
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

    @memoize
    def top_countries_by_export(self, year, k):
        all = [(self.total_exports(country, year), country) for country in self.countries()]
        all.sort()
        size = len(all)
        topK = all[size - k:size]
        topK.reverse()
        return [c for v, c in topK]

    def _load_row(self, exporter, importer, row_map, year_columns=YEAR_COLUMNS):
        for column in year_columns:
            export_quantity = row_map.get(column)
            year = column_to_year(column)
            if not year in self.all_years:
                continue
            if export_quantity == 'NaN':
                self.__record_nan_data(year, exporter, importer)
            else:
                self.__export_data_for_a_country(exporter, year).set_export_to_country(importer,
                    float(export_quantity))
            self.all_countries[exporter] = 1
            self.all_countries[importer] = 1
            print "in " + str(year) + ", " + exporter + " exported " + export_quantity + " to " + importer

    def load_file(self, file_path, year_columns=YEAR_COLUMNS, should_read_world_datapoints=False):
        f = open(file_path, 'rb')
        reader = csv.DictReader(f, skipinitialspace=True)

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
            self._load_row(exporter, importer, row, year_columns)
        f.close()

    @memoize
    def __trade_exists(self, exporter, importer):
        return self.export_data(1999, exporter, importer, return_this_for_missing_datapoint=-1) != -1

    def _trade_exists(self, year, exporter, importer):
        return self.__trade_exists(exporter, importer)

    def __record_nan_data(self, year, exporter, importer):
        m = self.nan_records_map[year]
        self.__export_data_for_a_country(exporter, year).set_export_to_country(importer, 0)
        if exporter not in m:
            m[exporter] = {}
        m[exporter][importer] = 1

    def _is_nan(self, year, exporter, importer):
        m = self.nan_records_map[year]
        if exporter in m:
            if importer in m[exporter]:
                return True
        return False

    @memoize
    def first_trade_year(self, C1, C2):
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
        return retval

