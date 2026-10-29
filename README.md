# Data warehousing capstone: from an OLTP sales database to a star-schema warehouse and dashboards

Capstone of the IBM Data Warehouse Engineer Professional Certificate. The brief: SoftCart, an online retailer, needs its transactional sales data moved into a warehouse that answers questions by country, category and time. This repo holds the SQL, the load and export scripts, the ETL that keeps the warehouse in step with the OLTP system, and the screenshots submitted for grading.

The course runs on IBM Cloud (Db2, Cognos). This project was built with local equivalents so every step is reproducible on a laptop: **MySQL** for the OLTP database, **PostgreSQL** for the staging and production warehouses, and a Python-generated dashboard in place of Cognos.

## Modules

| Folder | Step | What is in it |
|---|---|---|
| `modules/module1_environment/` | OLTP database | `sales.sales_data` DDL, import of `oltpdata.csv`, index check, `datadump.sh` / `datadump.ps1` export with `mysqldump`; outputs in `outputs/` |
| `modules/module2_oltp_db_design/` | Warehouse design | Star schema for `softcart` (`DimDate`, `DimCategory`, `DimCountry`, `DimItem`, `FactSales`), a staging copy, loads of the dimension and fact CSVs, and the analytics queries: `GROUPING SETS`, `ROLLUP`, `CUBE` and a materialised aggregate (`total_sales_per_country`) |
| `modules/module3_staging_dw/` | Reporting | `generate_dashboard.py` builds the three charts asked for: month-wise sales for 2020 (line), category share (pie), quarterly mobile-phone sales (bar) |
| `modules/module4_production_dw/` | Incremental ETL | `ETL.sh` / `ETL.ps1` pull the last 24 hours of rows from MySQL (`extract.sql`, `mysql_last24h.tsv`) and append them to the PostgreSQL fact table (`stage.sql`, `factsales.sql`, `dimdate.sql`) |
| `final_submission/` | Grading pack | One screenshot per rubric item (`images/`) with `README_upload.md` describing each |
| `tools/` | Helpers | Scripts that load CSVs into MySQL, render result tables and generate the screenshots |

## Run it

```bash
# 1. OLTP
mysql -u root -p < modules/module1_environment/01_create_database.sql
mysql -u root -p < modules/module1_environment/02_sales_schema.sql
# import modules/module1_environment/oltpdata.csv into sales.sales_data, then
bash modules/module1_environment/datadump.sh

# 2. Warehouse
psql -U postgres -c "CREATE DATABASE softcart;"
psql -U postgres -d softcart -f modules/module2_oltp_db_design/sql/01_softcart_dw_schema.sql
psql -U postgres -d softcart -f modules/module2_oltp_db_design/queries/analytics.sql

# 3. Dashboard
python modules/module3_staging_dw/generate_dashboard.py

# 4. Incremental load
bash modules/module4_production_dw/downloaded/ETL.sh
```

Each module's own `README.md` lists the exact steps and the screenshots it produces. Database passwords are placeholders (`<your-password>`); set your own.

## Author

Omar Essam El Sherbiny: [website](https://omaressam.web.app) · [LinkedIn](https://www.linkedin.com/in/omar-essam-el-sherbiny-b602279b/)
