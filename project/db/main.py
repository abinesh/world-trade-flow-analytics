import csv
from project.config import WORLD_TRADE_FLOW_DATA_FILE, YEAR_COLUMNS

def print_sql_inserts(csv_file, sql_file):
    reader = csv.DictReader(open(csv_file, 'rb'), skipinitialspace=True)
    sql_out = open(sql_file, 'w')

    i = 0
    for row in reader:
        query = 'insert into export_data values('
        columns = []

        importer = row.get('Importer')
        exporter = row.get('Exporter')
        columns.append("'%s'" % exporter)
        columns.append("'%s'" % importer)
        for column in YEAR_COLUMNS:
            export_quantity = row.get(column)
            if export_quantity == 'NaN':
                columns.append("NULL")
            else:
                columns.append("%s" % export_quantity)
        query += ",".join(columns) + ');'
        print i
        i += 1
        sql_out.write(query + '\n')
    sql_out.close()


print_sql_inserts(WORLD_TRADE_FLOW_DATA_FILE, 'out/inserts.sql')