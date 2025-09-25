-- Adjust absolute path to your environment if needed
-- Place CSVs in modules/module2_oltp_db_design/data

\copy DimDate(dateid,date,year,quarter,quartername,month,monthname,day,weekday,weekdayname) FROM 'modules/module2_oltp_db_design/downloaded/DimDate.csv' DELIMITER ',' CSV HEADER;
\copy DimCategory(categoryid,categoryname) FROM 'modules/module2_oltp_db_design/downloaded/DimCategory.csv' DELIMITER ',' CSV HEADER;
\copy DimCountry(countryid,country) FROM 'modules/module2_oltp_db_design/downloaded/DimCountry.csv' DELIMITER ',' CSV HEADER;
\copy FactSales(orderid,dateid,countryid,categoryid,amount) FROM 'modules/module2_oltp_db_design/downloaded/FactSales.csv' DELIMITER ',' CSV HEADER;


