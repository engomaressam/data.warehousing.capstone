DROP TABLE IF EXISTS FactSales;
CREATE TABLE FactSales AS
SELECT 
  order_id    AS orderid,
  CAST(ts::date AS date) AS dateid,
  product_id, customer_id,
  quantity    AS quantity,
  0::numeric  AS amount
FROM sales_data;
