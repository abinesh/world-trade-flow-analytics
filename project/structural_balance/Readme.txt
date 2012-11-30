1. Count of missing data points per year
   select year,count(*) from export_data_column_wise where export_quantity is NULL group by year;
2. Count of missing data per country pair
   select exporter,importer,count(*) missing_data_point_count from export_data_column_wise where export_quantity is NULL group by exporter,importer order by missing_data_point_count;
