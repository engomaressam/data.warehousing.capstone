-- Quick checks to support screenshots
\dt
SELECT COUNT(*) AS dimdate_rows FROM DimDate;
SELECT COUNT(*) AS dimcategory_rows FROM DimCategory;
SELECT COUNT(*) AS dimcountry_rows FROM DimCountry;
SELECT COUNT(*) AS factsales_rows FROM FactSales;
SELECT * FROM DimDate ORDER BY dateid LIMIT 5;
SELECT * FROM DimCategory ORDER BY categoryid LIMIT 5;
SELECT * FROM DimCountry ORDER BY countryid LIMIT 5;
SELECT * FROM FactSales ORDER BY salesid LIMIT 5;


