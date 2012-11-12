from project import countries

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


def column_to_year(column):
    if column == "Value00":
        return 2000
    return 1900 + int(column[5:])


def export_data_for_a_country(exporter, year):
    country_index = countries.country_to_index_map[exporter]
    return years_map[year][country_index]


def export_data(year, exporter, importer):
    exporter_data_for_year = export_data_for_a_country(exporter, year)
    return exporter_data_for_year.get_export_to_country(importer)


