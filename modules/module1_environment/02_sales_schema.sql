-- Use the database
USE sales;

-- Drop and recreate table sales_data to match the real CSV (5 columns)
DROP TABLE IF EXISTS sales_data;

-- CSV columns: order_id, product_id, customer_id, quantity, ts
CREATE TABLE sales_data (
  order_id     INT NOT NULL,
  product_id   INT NOT NULL,
  customer_id  INT NOT NULL,
  quantity     INT NOT NULL,
  ts           DATETIME NOT NULL,
  INDEX idx_order_id(order_id),
  INDEX idx_product_id(product_id)
);

-- Task 6: Create an index on timestamp field (secondary index)
CREATE INDEX ts ON sales_data (ts);


