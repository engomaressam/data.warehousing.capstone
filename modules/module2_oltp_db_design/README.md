Module 2 - Data Warehousing (Local Postgres)

Local alternatives
- Staging/Data Warehouse: PostgreSQL (local)
- ERD: Use pgAdmin ERD or draw.io; SQL provided here mirrors a typical star schema

Databases
- softcart: star schema (dimensions + fact)
- staging: optional copy of schema for ingestion
- Test1: reporting lab database for loading CSVs

Steps
1) Ensure PostgreSQL is running and `psql` is in PATH. Local creds used: user `postgres`, password `PMO@1234`.
2) Create DBs:
   - psql -U postgres -c "CREATE DATABASE softcart;"
   - psql -U postgres -c "CREATE DATABASE staging;"
   - psql -U postgres -c "CREATE DATABASE \"Test1\";"
3) Apply schemas:
   - psql -U postgres -d softcart -f modules/module2_oltp_db_design/sql/01_softcart_dw_schema.sql
   - psql -U postgres -d staging -f modules/module2_oltp_db_design/sql/02_staging_schema.sql
   - psql -U postgres -d Test1 -f modules/module2_oltp_db_design/sql/03_test1_create_tables.sql
4) Load CSVs to Test1 (place CSVs in `modules/module2_oltp_db_design/data`):
   - psql -U postgres -d Test1 -f modules/module2_oltp_db_design/sql/04_test1_copy_commands.sql
5) Run analytics queries (in softcart/Test1 as appropriate):
   - psql -U postgres -d softcart -f modules/module2_oltp_db_design/queries/analytics.sql
6) Screenshot checklist outputs into `final_submission/images/`:
   - softcartDimDate.jpg, dimtables.jpg, softcartFactSales.jpg, softcartRelationships.jpg
   - createschema.jpg
   - DimDate.jpg, DimCategory.jpg, DimCountry.jpg, FactSales.jpg
   - groupingsets.jpg, rollup.jpg, cube.jpg, mqt.jpg


