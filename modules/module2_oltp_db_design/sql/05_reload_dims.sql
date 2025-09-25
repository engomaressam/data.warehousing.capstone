TRUNCATE FactSales, DimCategory, DimCountry RESTART IDENTITY;
\copy DimCategory(categoryid,categoryname) FROM 'modules/module2_oltp_db_design/downloaded/DimCategory.csv' DELIMITER ',' CSV HEADER;
\copy DimCountry(countryid,country) FROM 'modules/module2_oltp_db_design/downloaded/DimCountry.csv' DELIMITER ',' CSV HEADER;
\copy FactSales(orderid,dateid,countryid,categoryid,amount) FROM 'modules/module2_oltp_db_design/downloaded/FactSales.csv' DELIMITER ',' CSV HEADER;


