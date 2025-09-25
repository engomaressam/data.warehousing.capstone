CREATE TABLE IF NOT EXISTS sales_data (
  order_id     INT NOT NULL,
  product_id   INT NOT NULL,
  customer_id  INT NOT NULL,
  quantity     INT NOT NULL,
  ts           TIMESTAMP NOT NULL
);
TRUNCATE sales_data;
