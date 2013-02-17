from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_D, NEGATIVE_LINK, POSITIVE_LINK, args_for_definition_D, NO_LINK
from project.structural_balance.plots.config import OUT_DIR
from project.util import file_safe

thresholds = [99, 95, 90, 85, 80]
a_few_years = [1969, 1979, 1988, 1989, 1990, 1999, 2000]
a_few_countries = ['Iran', 'USA', 'UK', 'Australia', 'France,Monac', 'China', 'Bangladesh', 'Sri Lanka']

def generate_matlab_histogram_code(data, thresholds=thresholds, years=a_few_years, countries=a_few_countries):
#USA, UK, Australia, France, China, Iran, Bangladesh, Srilanka
#1969,1979,1989,1999,2000
# cutoff threshold 99,95,90,85,80
#    todo: slanted x axis labels or inline labels, colour to separate top 90% bars
    for percentile_threshold in thresholds:
        for year in years:
            for A in countries:
                (line1, line2, line3) = ('x=[', 'x1=[', 'y={')
                (sum, count, previous_value, in_pruned_zone, positives_count) = (0, 0, -1, False, 0)

                for entry in data.countries_sorted_by_export_percentages(A, year, countries):
                    current_value = float(entry[1])
                    if "%.2f" % current_value == "0.00": break
                    sum += current_value
                    count += 1

                    line2_value = 0
                    if sum > percentile_threshold and not in_pruned_zone:
                        if current_value == previous_value:
                            line2_value = 0
                        else:
                            line2_value = 10
                            in_pruned_zone = True
                    if not in_pruned_zone: positives_count += 1

                    line1 = "%s %.2f " % (line1, entry[1])
                    line2 = "%s %d " % (line2, line2_value)
                    line3 = "%s, '%s'" % (line3, entry[0])

                    previous_value = current_value

                if count == 0: continue
                line1 = "%s]';" % line1
                line2 = "%s]';" % line2
                line3 = "%s};" % line3
                print line1
                print line2
                print line3
                print "bar(1:%d,[x x1],0.5,'stack');" % count
                print "set(gca,'XTickLabel',y);"
                #                print "text(30,0,y(:,1:%d));" % positives_count if positives_count < 50 else 50
                #                print "text(30,0,y(:,1:20))"
                #                print "set(gca,'XTick',0:5:length(x));"
                print "saveas(gcf,'%s-%d-%d','png');" % (A, percentile_threshold, year)


def print_graph_densities_for_different_thresholds(data, thresholds, years):
    f = open(OUT_DIR.DEFINITION_D + 'combinations.txt', 'w')
    for T in thresholds:
        for year in years:
            positive_edges = 0
            negative_edges = 0
            for (A, B) in countries.country_pairs(data.countries()):
                link_sign = definition_D(data, year, A, B, args_for_definition_D(T, log_file=f))
                if link_sign == POSITIVE_LINK: positive_edges += 1
                if link_sign == NEGATIVE_LINK: negative_edges += 1
            N = 203
            density = 2.0 * (positive_edges + negative_edges) / (N * (N - 1)) * 100
            print "%d,%d,%f,%d,%d,%d" % (T, year, density, positive_edges, negative_edges, N)
    f.close()


def print_histogram_as_text(data, years, countries):
    args = args_for_definition_D(99, mode='one-way')
    f = open(OUT_DIR.DEFINITION_D + 'def_d_db.txt', 'w')
    for year in years:
        for A in countries:
            (sum, count, previous_value, in_pruned_zone, positives_count) = (0, 0, -1, False, 0)
            file_entry = []

            for entry in data.countries_sorted_by_export_percentages(A, year, countries):
                current_value = float(entry[1])
                if "%.2f" % current_value == "0.00": break
                sum += current_value
                count += 1

                def link_sign(link):
                    if link == POSITIVE_LINK: return '+'
                    if link == NEGATIVE_LINK: return '-'
                    if link == NO_LINK: return 'M'

                #            file_entry = [('USA', 10, 10,+), ('UK', 10, 20,+), ('Japan', 10, 30,-)]
                file_entry.append((entry[0], entry[1], sum, link_sign(definition_D(data, year, A, entry[0], args))))

            if count == 0: continue
            f.write("%d:%s:[%s]\n" % (year, A, ','.join(["(%s,%.2f,%.2f,%s)" % (country, percentage, percentile, sign)
                                                         for(country, percentage, percentile, sign) in file_entry])))

    f.close()


def print_missing_links_db(data, year, T, log_file_name):
    two_way_args = args_for_definition_D(T)
    one_way_args = args_for_definition_D(T, mode='one-way')
    count = 0
    f = open(OUT_DIR.DEFINITION_D + log_file_name, 'w')
    for (A, B) in countries.country_pairs(data.countries()):
        if definition_D(data, year, A, B, two_way_args) == NO_LINK:
            one_way = definition_D(data, year, A, B, one_way_args)
            other_way = definition_D(data, year, B, A, one_way_args)
            f.write("Y%d,%s,%s,%s,%s\n" % (year, file_safe(A), file_safe(B), one_way, other_way))
            if one_way != other_way:
                for Y in range(1963, 2001):
                    f.write("%d,%s,%s,%s,%s\n" % (
                        Y, file_safe(A), file_safe(B),
                        data.export_data_as_percentile(year, A, B),
                        data.export_data_as_percentile(year, B, A)))
                    count += 1
                    if count == 5000: break
    f.close()


data = None
data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

#generate_matlab_histogram_code(data, [99], [2000], ['Georgia', 'USA'])
#print_histogram_as_text(data, a_few_years, data.countries())
print_missing_links_db(data, 2000, 99, 'def_d_db_hist.txt')
#print_graph_densities_for_different_thresholds(data, thresholds, a_few_years)


