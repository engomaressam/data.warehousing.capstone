$ErrorActionPreference = 'Stop'

# Config
$mysqlExe = 'C:/Program Files/MySQL/MySQL Server 8.0/bin/mysql.exe'
$mysqldumpExe = 'C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe'
$mysqlUser = 'root'
$mysqlPwd  = 'PMO@1234'
$mysqlDb   = 'sales'

$psqlExe   = 'psql'
$pgUser    = 'postgres'
$pgDb      = 'staging'

$work      = Join-Path $PSScriptRoot 'work'
New-Item -ItemType Directory -Force -Path $work | Out-Null

# 1) Extract: pull last 24h rows from MySQL to a CSV
$extractSql = @"
SET SESSION time_zone = '+00:00';
SELECT order_id,product_id,customer_id,quantity,DATE_FORMAT(ts,'%Y-%m-%d %H:%i:%s') AS ts
FROM sales.sales_data
WHERE ts >= NOW() - INTERVAL 1 DAY;
"@
Set-Content -Path (Join-Path $work 'extract.sql') -Value $extractSql -Encoding UTF8
Get-Content (Join-Path $work 'extract.sql') | & $mysqlExe -u $mysqlUser -p$mysqlPwd --batch --raw --skip-column-names | Out-File -FilePath (Join-Path $work 'mysql_last24h.tsv') -Encoding ASCII

# Convert TSV to CSV
(Get-Content (Join-Path $work 'mysql_last24h.tsv')) | ForEach-Object { $_ -replace "\t", "," } | Set-Content -Path (Join-Path $work 'mysql_last24h.csv') -Encoding ASCII

# 2) Load into Postgres staging.sales_data
$createStage = @"
CREATE TABLE IF NOT EXISTS sales_data (
  order_id     INT NOT NULL,
  product_id   INT NOT NULL,
  customer_id  INT NOT NULL,
  quantity     INT NOT NULL,
  ts           TIMESTAMP NOT NULL
);
TRUNCATE sales_data;
"@
Set-Content -Path (Join-Path $work 'stage.sql') -Value $createStage -Encoding UTF8
& $psqlExe -U $pgUser -d $pgDb -f (Join-Path $work 'stage.sql')
& $psqlExe -U $pgUser -d $pgDb -c "\copy sales_data(order_id,product_id,customer_id,quantity,ts) FROM '$(Join-Path $work 'mysql_last24h.csv')' DELIMITER ',' CSV"

# 3) Transform -> DimDate
$dimDate = @"
DROP TABLE IF EXISTS DimDate;
CREATE TABLE DimDate AS
SELECT DISTINCT
  CAST(ts::date AS date)                  AS dateid,
  EXTRACT(year   FROM ts)::int            AS year,
  EXTRACT(quarter FROM ts)::int           AS quarter,
  TO_CHAR(ts, 'Mon')                      AS monthname,
  EXTRACT(month  FROM ts)::int            AS month,
  EXTRACT(day    FROM ts)::int            AS day,
  EXTRACT(dow    FROM ts)::int            AS weekday,
  TO_CHAR(ts, 'Day')                      AS weekdayname
FROM sales_data;
"@
Set-Content -Path (Join-Path $work 'dimdate.sql') -Value $dimDate -Encoding UTF8
& $psqlExe -U $pgUser -d $pgDb -f (Join-Path $work 'dimdate.sql')

# 4) Transform -> FactSales
$fact = @"
DROP TABLE IF EXISTS FactSales;
CREATE TABLE FactSales AS
SELECT 
  order_id    AS orderid,
  CAST(ts::date AS date) AS dateid,
  product_id, customer_id,
  quantity    AS quantity,
  0::numeric  AS amount
FROM sales_data;
"@
Set-Content -Path (Join-Path $work 'factsales.sql') -Value $fact -Encoding UTF8
& $psqlExe -U $pgUser -d $pgDb -f (Join-Path $work 'factsales.sql')

# 5) Export DimDate and FactSales
$dimCsv = Join-Path $PSScriptRoot 'DimDate.csv'
$factCsv = Join-Path $PSScriptRoot 'FactSales.csv'
& $psqlExe -U $pgUser -d $pgDb -c "\copy DimDate TO '$dimCsv' DELIMITER ',' CSV HEADER"
& $psqlExe -U $pgUser -d $pgDb -c "\copy FactSales TO '$factCsv' DELIMITER ',' CSV HEADER"

Write-Host 'ETL completed'


