from project import countries
from scipy.sparse import csc_matrix
import scipy

#todo: Merge lower_bound and upper_bound to single value
def strong_tie_def_args(lower_bound, upper_bound):
    return {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }


def is_there_a_strong_tie_method_B(data, year, exporter, importer, def_args):
    val = data.export_import_ratio(exporter, importer, year)
    if val == -1:
        return False
    return def_args['lower_bound'] <= val <= def_args['upper_bound']


def get_relationship_matrix(data, year, relationship_definition, def_args):
    array_data = []
    for export_country in countries.countries:
        row = []
        for import_country in countries.countries:
            if relationship_definition(data, year, export_country, import_country, def_args):
                row.append(1)
            else:
                row.append(0)
        array_data.append(row)
    a = scipy.array(array_data)
    b = scipy.asmatrix(a)
    return b


def number_of_traids_for_a_country(dense_cube_matrix, country):
    index = countries.country_to_index_map[country]
    return int(dense_cube_matrix.tolist()[index][index])


def number_of_traids(dense_cube_matrix):
    total = 0
    for C in countries.world_excluded_countries_list():
        total += number_of_traids_for_a_country(dense_cube_matrix, C)
    return total / 6.0


def number_of_degrees(dense_matrix, row_country):
    matrix_as_list = dense_matrix.tolist()
    row_country_index = countries.country_to_index_map[row_country]
    degree = 0
    for column_country in countries.countries:
        column_country_index = countries.country_to_index_map[column_country]
        val = int(matrix_as_list[row_country_index][column_country_index])
        if val == 1:
            degree += 1
    return int(degree)


def __matrix_cube(dense_matrix):
    sparse_matrix = csc_matrix(dense_matrix)
    cube_matrix = sparse_matrix * sparse_matrix * sparse_matrix
    return cube_matrix.todense()


def graph_data(matrix):
    return (('Country', 'Traids', 'Degree'),
            [(country, number_of_traids_for_a_country(__matrix_cube(matrix), country),
              number_of_degrees(matrix, country)) for country
             in
             countries.countries])
