$ErrorActionPreference = 'Stop'

# Export all rows in sales.sales_data to sales_data.sql (PowerShell)
$env:MYSQL_PWD = 'PMO@1234'
& mysqldump -u root --databases sales --tables sales_data | Set-Content -Path 'sales_data.sql' -Encoding UTF8


