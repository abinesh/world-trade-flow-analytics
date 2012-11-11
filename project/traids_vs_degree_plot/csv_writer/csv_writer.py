import csv

def csv_write(file, graph_data):
    print "writing to " + file
    with open(file, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_ALL)
        ((header1, header2, header3), data) = graph_data
        writer.writerow([header1, header2, header3])
        for row in data:
            (c1, c2, c3) = row
            writer.writerow([c1, c2, c3])