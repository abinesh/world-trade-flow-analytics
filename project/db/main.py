import csv
from project.config import YEAR_COLUMNS, WORLD_TRADE_FLOW_DATA_FILE_CLEANED
from project.util import column_to_year

def print_sql_inserts(csv_file, sql_file):
    reader = csv.DictReader(open(csv_file, 'rb'), skipinitialspace=True)
    sql_out = open(sql_file, 'w')

    i = 0
    for row in reader:
        table1_query = 'insert into export_data_row_wise values('
        columns = []

        importer = row.get('Importer')
        exporter = row.get('Exporter')
        columns.append("'%s'" % exporter)
        columns.append("'%s'" % importer)
        for column in YEAR_COLUMNS:
            export_quantity = row.get(column)
            val = "NULL" if export_quantity == 'NaN' else export_quantity

            sql_out.write("insert into export_data_column_wise values('%s','%s','Y%d',%s);\n" % (exporter, importer,
                                                                                             column_to_year(column),
                                                                                             val))
            columns.append(val)
        table1_query += ",".join(columns) + ');'
        print i
        i += 1
        sql_out.write(table1_query + '\n')
    sql_out.close()


print_sql_inserts(WORLD_TRADE_FLOW_DATA_FILE_CLEANED, 'out/inserts.sql')