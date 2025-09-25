-- Module 2: Data Warehousing (PostgreSQL)
-- Database: softcart (star schema design)

-- Create database note: run separately if needed:
--   CREATE DATABASE softcart;
--   \c softcart

-- Dimensions
CREATE TABLE IF NOT EXISTS softcartDimDate (
  dateid        DATE PRIMARY KEY,
  year          INTEGER NOT NULL,
  quarter       INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
  month         INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
  monthname     VARCHAR(20) NOT NULL,
  day           INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
  weekday       INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
  weekdayname   VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS softcartDimCategory (
  categoryid    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  categoryname  VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS softcartDimItem (
  itemid        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  sku           VARCHAR(50) NOT NULL,
  title         VARCHAR(200) NOT NULL,
  categoryid    INTEGER NOT NULL REFERENCES softcartDimCategory(categoryid)
);

CREATE TABLE IF NOT EXISTS softcartDimCountry (
  countryid     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  country       VARCHAR(100) NOT NULL
);

-- Fact
CREATE TABLE IF NOT EXISTS softcartFactSales (
  salesid       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  dateid        DATE NOT NULL REFERENCES softcartDimDate(dateid),
  itemid        INTEGER NOT NULL REFERENCES softcartDimItem(itemid),
  countryid     INTEGER NOT NULL REFERENCES softcartDimCountry(countryid),
  quantity      INTEGER NOT NULL,
  unitprice     NUMERIC(12,2) NOT NULL,
  totalsales    NUMERIC(14,2) NOT NULL
);

-- Useful indexes
CREATE INDEX IF NOT EXISTS idx_factsales_date ON softcartFactSales(dateid);
CREATE INDEX IF NOT EXISTS idx_factsales_item ON softcartFactSales(itemid);
CREATE INDEX IF NOT EXISTS idx_factsales_country ON softcartFactSales(countryid);


