Module 1 - Environment and OLTP (Local Alternatives)

- OLTP: MySQL (local)
- Staging DW: PostgreSQL (local)
- Production DW: Local PostgreSQL used instead of DB2 on Cloud
- BI: Use a local tool (e.g., Metabase) instead of Cognos

Steps
1. Start MySQL and ensure `mysql` and `mysqldump` are in PATH.
2. Create DB and table:
   - mysql -u root -pPMO@1234 < modules/module1_environment/01_create_database.sql
   - mysql -u root -pPMO@1234 < modules/module1_environment/02_sales_schema.sql
3. Import `oltpdata.csv` into `sales.sales_data` via phpMyAdmin/DBeaver or CLI.
4. Verify index:
   - SHOW INDEX FROM sales.sales_data;
5. Export data:
   - Bash: bash modules/module1_environment/datadump.sh
   - PowerShell: pwsh modules/module1_environment/datadump.ps1

Screenshots to capture (save in `final_submission/images/`)
- createtable.jpg (create table SQL and output)
- importdata.jpg (phpMyAdmin import status)
- listtables.jpg (list tables)
- salesrows.jpg (row count)
- listindexes.jpg (index list)
- exportdata.jpg (export script and output)


