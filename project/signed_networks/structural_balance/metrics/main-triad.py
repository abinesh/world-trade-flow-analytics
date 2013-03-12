from itertools import combinations
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.structural_balance.metrics.triad import triad_type
from project.signed_networks.structural_balance.metrics.config import OUT_DIR
from project.util import file_safe


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)


def traid_plot_value(traid_type):
    if traid_type == 'T003':
        return 0
    elif traid_type == 'T012':
        return 1
    elif traid_type == 'T102':
        return 2
    elif traid_type == 'T021':
        return 3
    elif traid_type == 'T111':
        return 4
    elif traid_type == 'T201':
        return 5
    elif traid_type == 'T030':
        return 6
    elif traid_type == 'T120':
        return 7
    elif traid_type == 'T210':
        return 8
    elif traid_type == 'T300':
        return 9
    print "traid_type=%s" % traid_type


f = open(OUT_DIR + 'triad-matlab-code.txt', 'w')
args = args_for_definition_C(10, 1000)

for (A, B, C) in combinations(data.countries(), 3):
    f.write("%s-%s-%s:y=%s\n" % (file_safe(A), file_safe(B), file_safe(C),
                                 str([traid_plot_value(
                                     triad_type(data, year, A, B, C, definition_C3, args))
                                      for year in data.all_years]).replace(",", " ")))
f.write("x=%s;\n" % str([year for year in data.all_years]).replace(",", " "))
f.write("plot(x,y,'b-o',[2000 2000],[0 8],'b.');\n")
f.write("set(gca,'YTick',[0 1 2 3 4 5 6 7 8 9]);\n")
f.write("set(gca,'YTickLabel',{'T003','T012','T102','T021','T111','T201','T030','T120','T210','T300'});\n")

f.close()