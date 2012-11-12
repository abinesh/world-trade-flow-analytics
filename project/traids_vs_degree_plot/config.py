WORLD_TRADE_FLOW_DATA_FILE = '../../dataset/wtf_bilat.csv'
WRITE_OUT_TO_DIR = 'out/'

YEAR_COLUMNS = ["Value63", "Value64", "Value65", "Value66", "Value67", "Value68", "Value69", "Value70", "Value71",
                "Value72", "Value73", "Value74", "Value75", "Value76", "Value77", "Value78", "Value79", "Value80",
                "Value81", "Value82", "Value83", "Value84", "Value85", "Value86", "Value87", "Value88", "Value89",
                "Value90", "Value91", "Value92", "Value93", "Value94", "Value95", "Value96", "Value97", "Value98",
                "Value99", "Value00"]

STRONG_TIES_LOWER_BOUND = 0.5
STRONG_TIES_UPPER_BOUND = 2

def graph_data_file_name(year):
    return WRITE_OUT_TO_DIR + 'traids-degrees-plot' + str(year)+'.csv'