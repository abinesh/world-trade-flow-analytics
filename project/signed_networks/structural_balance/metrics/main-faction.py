from numpy import corrcoef
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import falklands_war_countries, falkland_related_war_countries, iran_iraq_countries, warsaw_czechslovakia_invasion
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.structural_balance.metrics.config import OUT_DIR
from project.signed_networks.structural_balance.metrics.faction import positives_and_negatives_matrix_matlab, adjacency_matrix_matlab, positives_and_negatives_matrix, adjacency_matrix, adjacency_matrix_row, matrix_py_matlab_with_name, DEFAULT_COUNTRIES_LIST, concat_countries, matrix_py_to_matlab, export_volume_matrix


def detect_community(correlation, threshold):
    result = []
    for i in range(0, len(correlation)):
        community = sorted([(countries.index_to_country_map[j], correlation[i][j])
                            for j in range(0, len(correlation)) if i != j and correlation[i][j] > threshold],
                           key=lambda t: -t[1])
        result.append([(a, float("%.2f" % b)) for (a, b) in community])
    return result


def transform_pn_to_01(matrix, threshold):
    return [(1 if cell > threshold else 0 for cell in row) for row in matrix]


def adjacency_rcm_ordered(data_matrix, threshold, countries, file_prefix, ordered=True):
    '''
    r = [1 2 3 4 5 6 7 8 9 10]
    allowedR = [1 2 3 4 5 6]
    orderedVector = {'Argentina', 'Brazil', 'Fm USSR', 'Peru', 'Libya', 'Israel', 'UK', 'USA', 'Denmark', 'Portugal', 'Norway', 'Sweden'};
    filteredLabels = {};
    filteredR = []
    r_size = size(r)
    r_size = r_size(2)
    filteredRIndex = 1
    for i=1:r_size
        if ismember(r(i), allowedR)
            filteredR = [filteredR r(i)]
            filteredLabels{filteredRIndex} = char(orderedVector(r(i)));
            filteredRIndex = filteredRIndex + 1
        end
    end
    '''
    assert len(data_matrix) == len(data_matrix[0])
    all_countries = countries[0]
    allowed_countries = countries[1]
    lines = []
    lines.append(matrix_py_matlab_with_name('c0', transform_pn_to_01(data_matrix, threshold)))
    lines.append(matrix_py_matlab_with_name('datamatrix', data_matrix))
    lines.append("r = symrcm(c0);")
    lines.append(
        "allowedR = %s;" % (str([all_countries.index(country) + 1 for country in allowed_countries]).replace(",", "")))
    lines.append("countriesVectorRow={%s};" % (str(all_countries)[1:-1]))
    lines.append("filteredLabels = {};")
    lines.append("filteredR = []")
    lines.append("r_size = size(r)")
    lines.append("r_size = r_size(2)")
    lines.append("filteredRIndex = 1")
    lines.append("for i=1:r_size")
    lines.append("\tif ismember(r(i), allowedR)")
    lines.append("\t\tfilteredR = [filteredR r(i)]")
    lines.append("\t\tfilteredLabels{filteredRIndex} = char(countriesVectorRow(r(i)));")
    lines.append("\t\tfilteredRIndex = filteredRIndex + 1")
    lines.append("\tend")
    lines.append("end")

    lines.append("x=redgreencmap(200);")
    vectorName = 'filteredLabels' if ordered else 'countriesVectorRow'
    lines.append(
        "hm = HeatMap(datamatrix%s,'RowLabels',%s,'ColumnLabels',%s, 'Colormap', horzcat(horzcat(x(:,2),x(:,1)),x(:,3)));"
        % ('(filteredR,filteredR)' if ordered else '', vectorName, vectorName)
    )
    lines.append("plot(hm);")
    lines.append(
        "saveas(gcf,'%s-%d-%s','png');" % (file_prefix, threshold * 100, 'ordered' if ordered else 'unordered'))
    lines.append("close all force;")
    return lines


def write_matlab_code_for_rcm(data, definition, def_args, countries=DEFAULT_COUNTRIES_LIST):
    f = open(OUT_DIR.RCM_MATRIC + 'code.m', 'w')
    for year in [1965, 1970, 1975, 1980, 1985, 1990, 1995, 1999, 2000]:
        for coeff in range(0, 11):
            c = coeff * .05
            adj_matrix = adjacency_matrix(data, definition, def_args, year, countries)
            for line in adjacency_rcm_ordered(corrcoef(adj_matrix), c, [countries, countries]):
                f.write(line + "\n")
    f.close()


def list_as_matlab_vector(var_name, elements): return "%s={%s};" % (var_name, str(elements)[1:-1])


def write_matlab_code_for_corrmatrix(data, years, definition, def_args, file_prefix,
                                     countries=DEFAULT_COUNTRIES_LIST,
                                     country_study=False):
    for year in years:
        corrcoef_mat = corrcoef(adjacency_matrix(data, definition, def_args, year, countries))
        print matrix_py_matlab_with_name('corrmatrix%d' % year, corrcoef_mat, country_study)
    print "corrmatrix=[%s]" % (';'.join(['corrmatrix%d' % year for year in years]))
    print list_as_matlab_vector('countriesVectorColumn', countries)
    if country_study:
        print "countriesVectorRow={%s};" % (str(concat_countries([countries[0]], years))[1:-1])
    else:
        print "countriesVectorRow={%s};" % (str(concat_countries(countries, years))[1:-1])
    print "x=redgreencmap(200);"
    print "HeatMap(corrmatrix,'RowLabels',countriesVectorRow,'ColumnLabels',countriesVectorColumn, 'Colormap', horzcat(horzcat(x(:,2),x(:,1)),x(:,3)));"
    print "saveas(gcf,'%s','png');" % (file_prefix)


def write_correlation_list(file_name, matrix, threshold):
    f = open(OUT_DIR.CORRELATION_LIST + file_name, 'w')
    count = 0
    for row in detect_community(corrcoef(matrix), threshold):
        f.write("%d:%s,%d,%s\n" % (count, countries.index_to_country_map[count], len(row), row))
        count += 1
    f.close()


def write_all_correlation_files(data, definition, def_args):
    window_size = 4
    for year in data.all_years:
        write_correlation_list('adj-y%d.txt' % year, adjacency_matrix(data, definition, def_args, year), 0)
        if 1963 + window_size <= year:
            write_correlation_list('pn-y%d-to-y%d.txt' % (year - window_size + 1, year),
                                   positives_and_negatives_matrix(data, definition, def_args,
                                                                  range(year - window_size + 1, year + 1)), 0.5)


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_C3
def_args = args_for_definition_C(10, 5000)

# print "xpn=[%s]" % positives_and_negatives_matrix_matlab(data, definition, def_args, [1981, 1982, 1983, 1984])
# print "xpn=[%s]" % adjacency_matrix_matlab(data, definition, def_args, 1980)
# print corrcoef(adjacency_matrix(data, definition, def_args, 1980))

# print corrcoef(transpose(positives_and_negatives_matrix(data, definition, def_args, [1981, 1982, 1983, 1984])))

'''
print "xad=[%s]" % adjacency_matrix_matlab(data, definition, def_args, 1982)
print corrcoef(adjacency_matrix(data, definition, def_args, 1982))

print adjacency_matrix_row(data, definition, def_args, 1970, "China")
print adjacency_matrix_row(data, definition, def_args, 1990, "China")

print data.countries()
'''

# f=
# count = 0
# for row in detect_community(corrcoef(adjacency_matrix(data, definition, def_args, 1980)), 0):
# for row in detect_community(corrcoef(adjacency_matrix(data, definition, def_args, 1972)), 0):
# for row in detect_community(corrcoef(positives_and_negatives_matrix(data, definition, def_args, [1964,1965,1966,1967])),0.5):
# for row in detect_community(corrcoef(positives_and_negatives_matrix(data, definition, def_args, [1968,1969,1970,1971])),0.5):
# for row in detect_community(corrcoef(positives_and_negatives_matrix(data, definition, def_args, [1972,1973,1974,1975])),0.5):
#     print ("%d:%s,%d,%s" % (count, countries.index_to_country_map[count], len(row), row))
#     count += 1

# f.close()

# write_all_correlation_files(data, definition, def_args)
# write_matlab_code_for_rcm(data, definition, def_args)
# write_matlab_code_for_corrmatrix(data, [1978, 1983, 1987], definition, def_args, 'falkland',falkland_related_war_countries)
# write_matlab_code_for_corrmatrix(data, [1975, 1985, 1991], definition, def_args, 'iran-iraq', iran_iraq_countries)
# write_matlab_code_for_corrmatrix(data, [1963, 1968, 1975], definition, def_args, 'warsaw-czech',warsaw_czechslovakia_invasion)
# write_matlab_code_for_corrmatrix(data, [1985, 1990], definition, def_args, 'china',
#                                  ['China', 'Indonesia', 'Thailand', 'Brazil', 'Australia', 'Turkey', 'Singapore', 'USA',
#                                   'UK', 'Fm USSR', 'Greece'], True)

def matlab_code_for_rcm_ordered_corr_coef_for_adjacency_matrix(data, definition, def_args):
    f = open(OUT_DIR.RCM_MATRIC + 'code1.m', 'w')
    countries_list = data.top_countries_by_export_all_year(50)
    for year in data.all_years:
        adj_matrix = adjacency_matrix(data, definition, def_args, year, countries_list)
        for line in adjacency_rcm_ordered(corrcoef(adj_matrix), 0, [countries_list, countries_list], '%s' % year, True):
            f.write("%s\n" % line)
    f.close()


def matlab_code_for_rcm_ordered_corr_coef_for_sliding_window_degree_matrix(data, definition, def_args,
                                                                           normalize_row_or_column):
    f = open(OUT_DIR.RCM_MATRIC + 'iraniraqpn.m', 'w')
    all_countries = DEFAULT_COUNTRIES_LIST
    allowed_countries = iran_iraq_countries
    # all_countries = ['USA', 'UK', 'Australia', 'Greece']
    # allowed_countries = ['Australia', 'Greece']
    window_size = 5
    for window_start_year in data.all_years:
        sliding_window = range(window_start_year, window_start_year + window_size)
        window_end_year = sliding_window[-1:][0]
        if window_end_year > 2000: break
        pn_matrix = positives_and_negatives_matrix(data, definition, def_args, sliding_window, all_countries,
                                                   normalize_row_or_column)
        f.write(matrix_py_matlab_with_name('pnmatrix', pn_matrix))
        data_matrix = corrcoef(pn_matrix)
        for threshold in [0]:
            for line in adjacency_rcm_ordered(data_matrix, threshold, [all_countries, allowed_countries],
                                              '%s-%s' % (window_start_year, window_end_year)):
                f.write("%s\n" % line)
    f.close()


def matlab_code_for_rcm_ordered_corr_coef_for_export_volume_matrix(data, normalize_row_or_column):
    f = open(OUT_DIR.RCM_MATRIC + 'iraniraqexport.m', 'w')
    all_countries = DEFAULT_COUNTRIES_LIST
    allowed_countries = iran_iraq_countries
    # all_countries = ['USA', 'UK', 'Australia', 'Greece']
    # allowed_countries = ['Australia', 'Greece']
    for year in data.all_years:
        pn_matrix = export_volume_matrix(data, year, all_countries, normalize_row_or_column)
        f.write(matrix_py_matlab_with_name('exportvolume', pn_matrix))
        data_matrix = corrcoef(pn_matrix)
        for threshold in [0]:
            for line in adjacency_rcm_ordered(data_matrix, threshold, [all_countries, allowed_countries],
                                              '%s' % (year)):
                f.write("%s\n" % line)
    f.close()


def matlab_code_for_rcm_ordered_corr_coef_for_adjacency_matrix(data, definition, def_args):
    f = open(OUT_DIR.RCM_MATRIC + 'iraniraqadj.m', 'w')
    all_countries = DEFAULT_COUNTRIES_LIST
    allowed_countries = iran_iraq_countries
    for year in data.all_years:
        data_matrix = adjacency_matrix(data, definition, def_args, year, all_countries)
        for line in adjacency_rcm_ordered(data_matrix, 0, [all_countries, allowed_countries], '%s' % year):
            f.write("%s\n" % line)
    f.close()


def write_adjacency_matrices(data, definition, def_args, countries_list=DEFAULT_COUNTRIES_LIST):
    f = open(OUT_DIR.ADJACENCY_MATRIX + 'adjall.m', 'w')
    f.write(list_as_matlab_vector('countries', countries_list) + '\n')
    for year in data.all_years:
        f.write('adj%d=[%s]\n' % (year, adjacency_matrix_matlab(data, definition, def_args, year, countries_list)))
    f.close()

# write_adjacency_matrices(data, definition, def_args)
# matlab_code_for_rcm_ordered_corr_coef_for_adjacency_matrix(data, definition, def_args)
# matlab_code_for_rcm_ordered_corr_coef_for_sliding_window_degree_matrix(data, definition, def_args, 'column')
# matlab_code_for_rcm_ordered_corr_coef_for_adjacency_matrix(data, definition, def_args)
matlab_code_for_rcm_ordered_corr_coef_for_export_volume_matrix(data, 'column')
