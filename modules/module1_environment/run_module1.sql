USE sales;
LOAD DATA LOCAL INFILE 'C:/Users/Diaa/data.warehousing.capstone/modules/module1_environment/oltpdata.csv'
INTO TABLE sales_data
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(order_id, product_id, customer_id, quantity, ts);


