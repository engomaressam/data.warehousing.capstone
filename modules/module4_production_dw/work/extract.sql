SET SESSION time_zone = '+00:00';
SELECT order_id,product_id,customer_id,quantity,DATE_FORMAT(ts,'%Y-%m-%d %H:%i:%s') AS ts
FROM sales.sales_data
WHERE ts >= NOW() - INTERVAL 1 DAY;
