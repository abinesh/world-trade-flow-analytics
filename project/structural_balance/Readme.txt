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
    B.
        -Each yearly graph represents positive, negative relationships/links between all pairs of countries. Missing links are taken into consideration too.
        -A relationship/link between two countries in a year are determined as follows:
            -Relationship is positive if both export_from_A_to_B trend and export_from_B_to_A trend are positive
            -Relationship is negative if one or both of the trends are negative
            -Relationship is missing if one or both of the trends are missing
        -Trends are determined using a variation of bollinger bands where linear fit is used instead of moving average. Sliding window size is 5 years
            -A trend is considered positive when one of the following conditions are met
                -Linear fit slope is positive and export_percentage is within the range
                -Linear fit slope is positive and export_percentage is above range
                -Linear fit slope is negative and export_percentage is above range
            -A trend is considered negative when one of the following conditions are met
                -Linear fit slope is positive and export_percentage is below the range
                -Linear fit slope is negative and export_percentage is within the upper range
                -Linear fit slope is negative and export_percentage is below the upper range
            -A trend is missing when one of the following conditions are met
                -If the ratio of import/export between the two countries is not within the range 0.5 and 2
                -No datapoint for the interested year
                -Not enough data points(there should be atleast 3 data points) in sliding window to compute bollinger bands
    C1. A->B is positive if A's export to B is above a percentage threshold. Else it is negative. Links with sum of A->B exports over time below threshold T2 are pruned out and considered missing.
       A->B and B->A relationships should be combined
    C2. A->B is positive if A's export to B is above a percentage threshold. Else it is negative. Links with number of missing/Nan datapoints for  A->B exports above threshold T2 are pruned out and considered missing.
       A->B and B->A relationships should be combined
    D. A->B is Positive if A's export to B is within top 90 percent of its exports. Else it is pruned out. If it is pruned after a non-zero data-point it is negative, else it is missing link
       A->B and B->A relationships should be combined

   (To generate count of edge pairs run the following:
   def_C1: cat definition_C1-combinations.txt | cut -d"," -f 1,4,5,6 | sort | uniq -c
   def_C2: cat definition_C2-combinations.txt | cut -d"," -f 1,4,5,6 | sort | uniq -c
   def_D:  cat combinations.txt | cut -d "," -f 1,4,5,6 | sort | uniq -c


5. Top 50 countries data
    https://docs.google.com/spreadsheet/ccc?key=0AtaB149ijWVNdGI3eTBaVGxZajZFQnFDY09URmtRYWc#gid=1