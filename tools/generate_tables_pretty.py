import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
from pathlib import Path

OUT = Path('final_submission/images')

def df_to_image(df: pd.DataFrame, title: str, filename: str):
    OUT.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(16, 9))
    plt.title(title, fontsize=18, weight='bold')
    plt.axis('off')
    tbl = plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.4)
    plt.savefig(OUT / filename, dpi=150, bbox_inches='tight')
    plt.close()

def main():
    # Use Test1 data which we loaded from CSVs
    conn = psycopg2.connect(dbname='test1', user='postgres', password='PMO@1234', host='localhost')
    with conn, conn.cursor() as cur:
        # Cube sample (limit to keep image tidy)
        cur.execute("""
            SELECT dd.year, dc.country, AVG(fs.amount) AS average_sales
            FROM factsales fs
            JOIN dimdate dd ON fs.dateid = dd.dateid
            JOIN dimcountry dc ON fs.countryid = dc.countryid
            GROUP BY CUBE (dd.year, dc.country)
            ORDER BY dd.year NULLS LAST, dc.country NULLS LAST
            LIMIT 12
        """)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        cube_df = pd.DataFrame(rows, columns=cols)
        df_to_image(cube_df, 'Cube: year, country, average sales', 'cube.png')

        # Total sales per country (top 10)
        cur.execute("""
            SELECT dc.country, SUM(fs.amount) AS total_sales
            FROM factsales fs
            JOIN dimcountry dc ON fs.countryid = dc.countryid
            GROUP BY dc.country
            ORDER BY total_sales DESC
            LIMIT 10
        """)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        mqt_df = pd.DataFrame(rows, columns=cols)
        df_to_image(mqt_df, 'MQT: total_sales_per_country (Top 10)', 'mqt.png')

if __name__ == '__main__':
    main()


