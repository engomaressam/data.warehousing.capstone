DROP TABLE IF EXISTS DimDate;
CREATE TABLE DimDate AS
SELECT DISTINCT
  CAST(ts::date AS date)                  AS dateid,
  EXTRACT(year   FROM ts)::int            AS year,
  EXTRACT(quarter FROM ts)::int           AS quarter,
  TO_CHAR(ts, 'Mon')                      AS monthname,
  EXTRACT(month  FROM ts)::int            AS month,
  EXTRACT(day    FROM ts)::int            AS day,
  EXTRACT(dow    FROM ts)::int            AS weekday,
  TO_CHAR(ts, 'Day')                      AS weekdayname
FROM sales_data;
