-- Create Test1 database tables per Module 2 reporting section
-- Run:
--   CREATE DATABASE "Test1";
--   \c Test1

DROP TABLE IF EXISTS FactSales;
DROP TABLE IF EXISTS DimCountry;
DROP TABLE IF EXISTS DimCategory;
DROP TABLE IF EXISTS DimDate;

CREATE TABLE IF NOT EXISTS DimDate (
  dateid        INTEGER PRIMARY KEY,
  date          DATE NOT NULL,
  year          INTEGER NOT NULL,
  quarter       INTEGER NOT NULL,
  quartername   VARCHAR(10) NOT NULL,
  month         INTEGER NOT NULL,
  monthname     VARCHAR(20) NOT NULL,
  day           INTEGER NOT NULL,
  weekday       INTEGER NOT NULL,
  weekdayname   VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS DimCategory (
  categoryid    INTEGER PRIMARY KEY,
  categoryname  VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS DimCountry (
  countryid     INTEGER PRIMARY KEY,
  country       VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS FactSales (
  orderid       INTEGER PRIMARY KEY,
  dateid        INTEGER NOT NULL REFERENCES DimDate(dateid),
  countryid     INTEGER NOT NULL REFERENCES DimCountry(countryid),
  categoryid    INTEGER NOT NULL REFERENCES DimCategory(categoryid),
  amount        NUMERIC(14,2) NOT NULL
);


