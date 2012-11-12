from project.config import WRITE_OUT_TO_DIR

STRONG_TIES_LOWER_BOUND = 0.5
STRONG_TIES_UPPER_BOUND = 2

def graph_data_file_name(year):
    return WRITE_OUT_TO_DIR + 'traids-degrees-plot' + str(year)+'.csv'