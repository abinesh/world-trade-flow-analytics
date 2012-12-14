1. Count of missing data points per year
   select year,count(*) from export_data_column_wise where export_quantity is NULL group by year;
2. Count of missing data per country pair
   select exporter,importer,count(*) missing_data_point_count from export_data_column_wise where export_quantity is NULL group by exporter,importer order by missing_data_point_count;
3. Find country pairs with dataholes. Example: in 1998,1999,2000, 1999 is NULL.

select * from (select A.exporter,A.importer,count(*) cccc from export_data_column_wise a,export_data_column_wise b
    where (b.export_quantity is NULL and b.year='Y1999')
    and A.exporter = B.exporter
    and A.importer = B.importer
    and a.year in ('Y1998','Y1999','Y2000')
    and ((a.year ='Y1998' and a.export_quantity is not NULL)
        or (a.year ='Y2000' and a.export_quantity is not NULL)
        or (a.year ='Y1999' and a.export_quantity is NULL)
        )
    group by A.exporter,A.importer) A where A.cccc = 3

4. Positive/negative links definition
    A. If ratio of import and exports is within 0.5 and 2, it is a positive link. On all other cases(ratio out of range, missing datapoint), it is negative link.
