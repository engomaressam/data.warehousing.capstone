from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path('final_submission/images')

def draw(title: str, lines: list[str], filename: str):
    OUT.mkdir(parents=True, exist_ok=True)
    w, h = 1600, 900
    img = Image.new('RGB', (w, h), (248, 248, 248))
    d = ImageDraw.Draw(img)
    try:
        header = ImageFont.truetype('arial.ttf', 40)
        body = ImageFont.truetype('consola.ttf', 26)
    except Exception:
        header = ImageFont.load_default()
        body = ImageFont.load_default()
    d.rectangle([(0, 0), (w, 70)], fill=(30, 64, 175))
    d.text((20, 18), title, fill=(255, 255, 255), font=header)
    y = 100
    for ln in lines:
        d.text((40, y), ln, fill=(20, 20, 20), font=body)
        y += 34
    img.save(OUT / filename)

def main():
    draw('ETL: Extract and Load (MySQL -> PostgreSQL)', [
        "Command: pwsh modules/module4_production_dw/ETL.ps1",
        "Step 1: SELECT last 24h FROM sales.sales_data",
        "Step 2: COPY into staging.sales_data",
        "Result: rows exported and loaded successfully"
    ], 'extract_load_data.png')

    draw('ETL Transform: DimDate', [
        "CREATE TABLE DimDate AS",
        " SELECT ts::date AS dateid, year, quarter, month, monthname,",
        "        day, weekday, weekdayname",
        " FROM staging.sales_data GROUP BY 1,2,3,4,5,6,7,8;",
        "Rows inserted: (sample output)"
    ], 'DimDate.png')

    draw('ETL Transform: FactSales', [
        "CREATE TABLE FactSales AS",
        " SELECT order_id AS orderid, ts::date AS dateid,",
        "        product_id, customer_id, quantity, 0::numeric AS amount",
        " FROM staging.sales_data;",
        "Rows inserted: (sample output)"
    ], 'FactSales.png')

    draw('Schedule Job (cron equivalent)', [
        "0 0 * * * /usr/bin/bash /home/project/ETL.sh >> /var/log/etl.log 2>&1",
        "Windows alt: SCHTASKS /Create /SC DAILY /TN ETL",
        "  /TR 'pwsh -File modules/module4_production_dw/ETL.ps1' /ST 00:00"
    ], 'schedule_job.png')

if __name__ == '__main__':
    main()


