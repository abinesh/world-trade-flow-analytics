from project import countries
from scipy.sparse import csc_matrix
import scipy

def is_there_a_strong_tie_method_B(exportdata,year, exporter, importer, lower_bound, upper_bound):
    num = exportdata.export_data(year, exporter, importer)
    den = exportdata.export_data(year, importer, exporter)
    if den == 0:
        return None
    val = num / den
    return lower_bound <= val <= upper_bound


def matrix_for_year_method_B(data,year, lower_bound, upper_bound):
    array_data = []
    for export_country in countries.countries:
        row = []
        for import_country in countries.countries:
            if is_there_a_strong_tie_method_B(data,year, export_country, import_country, lower_bound, upper_bound):
                row.append(1)
            else:
                row.append(0)
        array_data.append(row)
    a = scipy.array(array_data)
    b = scipy.asmatrix(a)
    return b


def number_of_traids(dense_matrix, country):
    index = countries.country_to_index_map[country]
    return int(dense_matrix.tolist()[index][index])


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


def matrix_cube(dense_matrix):
    sparse_matrix = csc_matrix(dense_matrix)
    cube_matrix = sparse_matrix * sparse_matrix * sparse_matrix
    return cube_matrix.todense()


def graph_data(matrix):
    return (('Country', 'Traids', 'Degree'),
            [(country, number_of_traids(matrix_cube(matrix), country), number_of_degrees(matrix, country)) for country
             in
             countries.countries])
