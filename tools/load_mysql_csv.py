import csv
import mysql.connector
from pathlib import Path

CSV_PATH = Path('modules/module1_environment/oltpdata.csv')

def main():
    conn = mysql.connector.connect(
        host='localhost', user='root', password='PMO@1234', database='sales'
    )
    conn.autocommit = False
    cur = conn.cursor()
    # Clear table
    cur.execute('TRUNCATE TABLE sales_data')

    with CSV_PATH.open('r', newline='') as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            # order_id, product_id, customer_id, quantity, ts
            rows.append((int(row[0]), int(row[1]), int(row[2]), int(row[3]), row[4]))
            if len(rows) >= 1000:
                cur.executemany(
                    'INSERT INTO sales_data (order_id, product_id, customer_id, quantity, ts) VALUES (%s,%s,%s,%s,%s)',
                    rows,
                )
                conn.commit()
                rows.clear()
        if rows:
            cur.executemany(
                'INSERT INTO sales_data (order_id, product_id, customer_id, quantity, ts) VALUES (%s,%s,%s,%s,%s)',
                rows,
            )
            conn.commit()

    # Outputs for screenshots
    cur.execute('SELECT COUNT(*) FROM sales_data')
    count = cur.fetchone()[0]
    print('ROW_COUNT', count)

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()


