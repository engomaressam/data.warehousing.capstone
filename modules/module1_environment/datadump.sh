#!/usr/bin/env bash
set -euo pipefail

# Export all rows in sales.sales_data to sales_data.sql
mysqldump -u root -p"PMO@1234" --databases sales --tables sales_data > sales_data.sql


