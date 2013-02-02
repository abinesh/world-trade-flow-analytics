from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_D, NEGATIVE_LINK, POSITIVE_LINK, args_for_definition_D
from project.structural_balance.plots.config import OUT_DIR

thresholds = [99, 95, 90, 85, 80]
a_few_years = [1969, 1979, 1988, 1989, 1990, 1999, 2000]

def generate_matlab_code(data):
#USA, UK, Australia, France, China, Iran, Bangladesh, Srilanka
#1969,1979,1989,1999,2000
# cutoff threshold 99,95,90,85,80
#    todo: slanted x axis labels or inline labels, colour to separate top 90% bars
    for percentile_threshold in thresholds:
        for year in a_few_years:
            for A in ['Iran', 'USA', 'UK', 'Australia', 'France,Monac', 'China', 'Bangladesh', 'Sri Lanka']:
                list = []
                for B in data.countries():
                    percentage = data.export_data_as_percentage(year, A, B, False)
                    if percentage is None: continue
                    list.append((B, 100 * percentage))

                (line1, line2, line3) = ('x=[', 'x1=[', 'y={')
                (sum, count, previous_value, in_pruned_zone, positives_count) = (0, 0, -1, False, 0)

                for entry in sorted(list, key=lambda country: 0 if country[1] is None else -country[1]):
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


def print_graph_densities_for_different_thresholds(data):
    f = open(OUT_DIR.DEFINITION_D + 'combinations.txt', 'w')
    for T in thresholds:
        for year in a_few_years:
            positive_edges = 0
            negative_edges = 0
            for (A, B) in countries.country_pairs(data.countries()):
                link_sign = definition_D(data, year, A, B, args_for_definition_D(T, f))
                if link_sign == POSITIVE_LINK: positive_edges += 1
                if link_sign == NEGATIVE_LINK: negative_edges += 1
            N = 203
            density = 2.0 * (positive_edges + negative_edges) / (N * (N - 1)) * 100
            print "%d,%d,%f,%d,%d,%d" % (T, year, density, positive_edges, negative_edges, N)
    f.close()

data = None
data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

#generate_matlab_code(data)
print_graph_densities_for_different_thresholds(data)


