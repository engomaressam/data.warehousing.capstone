-- Use database softcart before running these

-- Grouping sets: country, category, totalsales
SELECT dc.country AS country,
       cat.categoryname AS category,
       SUM(fs.totalsales) AS totalsales
FROM softcartFactSales fs
JOIN softcartDimCountry dc ON fs.countryid = dc.countryid
JOIN softcartDimItem it ON fs.itemid = it.itemid
JOIN softcartDimCategory cat ON it.categoryid = cat.categoryid
GROUP BY GROUPING SETS ((dc.country, cat.categoryname), (dc.country), (cat.categoryname), ());

-- Rollup: year, country, totalsales
SELECT dd.year,
       dc.country,
       SUM(fs.totalsales) AS totalsales
FROM softcartFactSales fs
JOIN softcartDimDate dd ON fs.dateid = dd.dateid
JOIN softcartDimCountry dc ON fs.countryid = dc.countryid
GROUP BY ROLLUP (dd.year, dc.country)
ORDER BY dd.year, dc.country;

-- Cube: year, country, average sales
SELECT dd.year,
       dc.country,
       AVG(fs.totalsales) AS average_sales
FROM softcartFactSales fs
JOIN softcartDimDate dd ON fs.dateid = dd.dateid
JOIN softcartDimCountry dc ON fs.countryid = dc.countryid
GROUP BY CUBE (dd.year, dc.country)
ORDER BY dd.year NULLS LAST, dc.country NULLS LAST;

-- Materialized View: total sales per country
DROP MATERIALIZED VIEW IF EXISTS total_sales_per_country;
CREATE MATERIALIZED VIEW total_sales_per_country AS
SELECT dc.country,
       SUM(fs.totalsales) AS total_sales
FROM softcartFactSales fs
JOIN softcartDimCountry dc ON fs.countryid = dc.countryid
GROUP BY dc.country;

-- Refresh example
-- REFRESH MATERIALIZED VIEW total_sales_per_country;


