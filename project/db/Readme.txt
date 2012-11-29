1. Create database
    Use create.sql

2. Insert data
    - Remove duplicates using the following
        cat wtf_bilat.csv | grep -v "Fm Yemen Dm\",\"218400\",\"USA\",NaN" | grep -v "Fm Yemen Dm\",\"100000\",\"World\",NaN" > wtf_bilat_cleaned.csv
    - run main.py to generate insert.sql
    - Use this sql to insert into mysql

3. Find missing data point count:
    - By Country,year
        select exporter,year,count(*) from export_Data_column_wise where export_quantity is NULL group by exporter, year;
    - By Year
        select year,count(*) from export_Data_column_wise where export_quantity is NULL group by year;
        select year,count(*) from export_Data_column_wise where year = 'Y2000' and export_quantity is NULL group by year;
