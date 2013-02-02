#Implementation of tables listed in paper http://www.cs.cornell.edu/home/kleinber/chi10-signed.pdf
from project import countries
from project.config import WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.export_data.strongties import get_relationship_matrix, number_of_traids_for_a_country
from project.export_data.exportdata import ExportData
from project.signed_networks.definitions import definition_C1, args_for_definition_C, NEGATIVE_LINK, POSITIVE_LINK, NO_LINK

def table1(data, year, definition, def_args):
    def link_exists_def(data, year, A, B, def_args1):
        return 0 if definition(data, year, A, B, def_args) == NO_LINK else 1

    edges_count, positive_edges_count, negative_edges_count, no_edge_count, traids = 0, 0, 0, 0, 0
    for (A, B) in countries.country_pairs(data.countries()):
        link_type = definition(data, year, A, B, def_args)
        if link_type == NEGATIVE_LINK: negative_edges_count += 1
        elif link_type == POSITIVE_LINK: positive_edges_count += 1
        elif link_type == NO_LINK: no_edge_count += 1
        edges_count += 1

    return {'Nodes': len(data.countries()),
            'Edges': edges_count,
            '+ edges': positive_edges_count * 100.0 / edges_count,
            '- edges': negative_edges_count * 100.0 / edges_count,
            'No edges': no_edge_count * 100.0 / edges_count,
                        'Traids': number_of_traids_for_a_country(get_relationship_matrix(data, year, link_exists_def, {}), 'USA')
    }


data = ExportData()
data.load_file('../' + WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_read_world_datapoints=True)
print table1(data, 2000, definition_C1, args_for_definition_C(5000, 1))
