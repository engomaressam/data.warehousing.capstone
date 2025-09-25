-- Create staging database and schema from ERD export
-- Run:
--   CREATE DATABASE staging;
--   \c staging

CREATE SCHEMA IF NOT EXISTS public;

-- Duplicate of softcart schema structure in staging for loads
CREATE TABLE IF NOT EXISTS softcartDimDate (LIKE softcart.public.softcartDimDate INCLUDING ALL);
CREATE TABLE IF NOT EXISTS softcartDimCategory (LIKE softcart.public.softcartDimCategory INCLUDING ALL);
CREATE TABLE IF NOT EXISTS softcartDimItem (LIKE softcart.public.softcartDimItem INCLUDING ALL);
CREATE TABLE IF NOT EXISTS softcartDimCountry (LIKE softcart.public.softcartDimCountry INCLUDING ALL);
CREATE TABLE IF NOT EXISTS softcartFactSales (LIKE softcart.public.softcartFactSales INCLUDING ALL);


