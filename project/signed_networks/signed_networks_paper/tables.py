#Implementation of tables listed in paper http://www.cs.cornell.edu/home/kleinber/chi10-signed.pdf
from project import countries
from project.export_data.strongties import number_of_traids, __matrix_cube, get_relationship_matrix
from project.signed_networks.definitions import NO_LINK, NEGATIVE_LINK, POSITIVE_LINK

def table1(data, year, definition, def_args):
    def link_exists_def(data, year, A, B, def_args1):
        if 'World' in [A, B]: return 0
        return 0 if definition(data, year, A, B, def_args) == NO_LINK else 1

    positive_edges_count, negative_edges_count, no_edge_count, traids = 0, 0, 0, 0
    for (A, B) in countries.country_pairs(data.countries()):
        link_type = definition(data, year, A, B, def_args)
        if link_type == NEGATIVE_LINK: negative_edges_count += 1
        elif link_type == POSITIVE_LINK: positive_edges_count += 1
        elif link_type == NO_LINK: no_edge_count += 1

    edges_count = positive_edges_count + negative_edges_count
    return {'Nodes': len(data.countries()),
            'Edges': edges_count,
            '+ edges': positive_edges_count * 100.0 / edges_count,
            '- edges': negative_edges_count * 100.0 / edges_count,
            'Traids': number_of_traids(__matrix_cube(get_relationship_matrix(data, year, link_exists_def, {})))
    }

