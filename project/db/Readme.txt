1. Create database
    Use create.sql

2. Insert data
    - Remove duplicates using the following
        cat wtf_bilat.csv | grep -v "Fm Yemen Dm\",\"218400\",\"USA\",NaN" | grep -v "Fm Yemen Dm\",\"100000\",\"World\",NaN" > wtf_bilat_cleaned.csv
    - run main.py to generate insert.sql
    - Use this sql to insert into mysql
