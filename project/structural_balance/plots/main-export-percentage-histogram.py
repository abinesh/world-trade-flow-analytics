from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData


def generate_matlab_code(data):
    #USA, UK, Australia, France, China, Iran, Bangladesh, Srilanka
    #1969,1979,1989,1999,2000
    # cutoff threshold 99,95,90,85,80
#    todo: slanted x axis labels or inline labels, colour to separate top 90% bars
    for percentile_threshold in [80, 85, 90, 95, 99]:
        for year in [1969, 1979, 1989, 1999, 2000]:
            for A in ['Iran', 'USA', 'UK', 'Australia', 'France,Monac', 'China', 'Bangladesh', 'Sri Lanka']:
                list = []
                for B in countries.world_excluded_countries_list():
                    percentage = data.export_data_as_percentage(year, A, B, False)
                    if percentage is None: continue
                    list.append((B, 100 * percentage))
                line1 = 'x=['
                line2 = 'y={'
                for a in sorted(list, key=lambda country: 0 if country[1] is None else -country[1]):
                    if int(a[1]) == 0: break
                    line1 = "%s %d " % (line1, a[1])
                    line2 = "%s, '%s'" % (line2, a[0])
                line1 = "%s]" % line1
                line2 = "%s}" % line2
                print line1
                print line2
                print "bar(x)"
                print "set(gca,'XTickLabel',y)"
                print "saveas(gcf,'%s-%d-%d','png')" % (A,percentile_threshold, year)

data = None
data = ExportData()
data.load_export_data('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

generate_matlab_code(data)
