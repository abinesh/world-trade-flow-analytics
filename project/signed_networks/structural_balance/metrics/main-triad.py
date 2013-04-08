from itertools import combinations
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C3, args_for_definition_C
from project.signed_networks.structural_balance.metrics.triad import triad_type, get_traids, is_traid
from project.signed_networks.structural_balance.metrics.config import OUT_DIR
from project.util import file_safe


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


def generate_triad_type_transition_matlab_code(data, definition, def_args):
    f = open(OUT_DIR.DIR + 'triad-matlab-code.txt', 'w')

    for (A, B, C) in combinations(data.countries(), 3):
        f.write("%s-%s-%s:y=%s\n" % (file_safe(A), file_safe(B), file_safe(C),
                                     str([traid_plot_value(
                                         triad_type(data, year, A, B, C, definition, def_args))
                                          for year in data.all_years]).replace(",", " ")))
    f.write("x=%s;\n" % str([year for year in data.all_years]).replace(",", " "))
    f.write("plot(x,y,'b-o',[2000 2000],[0 8],'b.');\n")
    f.write("set(gca,'YTick',[0 1 2 3 4 5 6 7 8 9]);\n")
    f.write("set(gca,'YTickLabel',{'T003','T012','T102','T021','T111','T201','T030','T120','T210','T300'});\n")

    f.close()


def print_traid_transitions(data, definition, def_args, years_range):
    for year in years_range:
        for traid in ['T0', 'T1', 'T2', 'T3']:
            this_year_count = 0
            next_year_counts = {'T0': 0, 'T1': 0, 'T2': 0, 'T3': 0}
            for (A, B, C) in get_traids(data, year, definition, def_args, traid):
                this_year_count += 1
                if is_traid(data, year, A, B, C, definition, def_args):
                    t_type = triad_type(data, year + 1, A, B, C, definition, def_args)[:2]
                    if t_type == 'T0': next_year_counts['T0'] += 1
                    if t_type == 'T1': next_year_counts['T1'] += 1
                    if t_type == 'T2': next_year_counts['T2'] += 1
                    if t_type == 'T3': next_year_counts['T3'] += 1
            for next_traid in ['T0', 'T1', 'T2', 'T3']:
                print "%d:%s->%s=%.2f" % (year, traid, next_traid, next_year_counts[next_traid] * 1.0 / this_year_count)


data = ExportData()
data.load_file('../../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)

definition = definition_C3
def_args = args_for_definition_C(10, 5000)

# generate_triad_type_transition_matlab_code(data,definition, def_args)

print_traid_transitions(data, definition, def_args, range(1995, 2001))

