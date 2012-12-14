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

4. Positive/negative links definitions
    A. If ratio of import and exports is within 0.5 and 2, it is a positive link. On all other cases(ratio out of range, missing datapoint), it is negative link.
    B. Link between two countries(A,B) in a year(Y) in a year is positive if both A->B trend and B->A trend are accelerating/stable-rising else it is either no_trend or decelerating/stable-falling
        a trend is stable-rising if linear fit slope is positive and export_quantity in a year is within bollinger band range considering last 5 years data
        a trend is stable-falling if linear fit slope is negative and export_quantity in a year is within bollinger band range ranges considering last 5 years data
        a trend is accelerating if export_quantity is above upper range
        a trend is decelerating if export_quantity is below lower range
        a trend doesn't exist if there is a missing data point in the sliding window period
