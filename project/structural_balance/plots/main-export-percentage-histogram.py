from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData


def generate_matlab_code(data):
#USA, UK, Australia, France, China, Iran, Bangladesh, Srilanka
#1969,1979,1989,1999,2000
# cutoff threshold 99,95,90,85,80
#    todo: slanted x axis labels or inline labels, colour to separate top 90% bars
    for percentile_threshold in [99,95,90,85,80]:
        for year in [1969, 1979, 1989, 1999, 2000]:
            for A in ['Iran', 'USA', 'UK', 'Australia', 'France,Monac', 'China', 'Bangladesh', 'Sri Lanka']:
                list = []
                for B in countries.world_excluded_countries_list():
                    percentage = data.export_data_as_percentage(year, A, B, False)
                    if percentage is None: continue
                    list.append((B, 100 * percentage))

                (line1, line2, line3) = ('x=[', 'x1=[', 'y={')
                (sum, count, previous_value, in_pruned_zone) = (0, 0, -1, False)

                for entry in sorted(list, key=lambda country: 0 if country[1] is None else -country[1]):
                    current_value = int(entry[1])
                    if current_value == 0: break
                    sum += current_value
                    count += 1

                    line2_value = 0
                    if sum > percentile_threshold and not in_pruned_zone:
                        if current_value == previous_value:
                            line2_value = 0
                        else:
                            line2_value = 10
                            in_pruned_zone = True

                    line1 = "%s %d " % (line1, entry[1])
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
                print "saveas(gcf,'%s-%d-%d','png');" % (A, percentile_threshold, year)

data = None
data = ExportData()
data.load_export_data('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

generate_matlab_code(data)
