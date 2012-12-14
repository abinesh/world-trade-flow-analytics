from project.export_data.strongties import is_there_a_strong_tie_method_B
from project.traids_vs_degree_plot.config import STRONG_TIES_LOWER_BOUND, STRONG_TIES_UPPER_BOUND

def definition_A(c1, c2, data, year):
    return "suit" if is_there_a_strong_tie_method_B(data, year, c1, c2, STRONG_TIES_LOWER_BOUND,
        STRONG_TIES_UPPER_BOUND) else "resolved"
