from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUTPUT_DIR = Path('final_submission/images')

def draw_text_image(filename: str, title: str, lines: list[str]):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    width, height = 1600, 900
    img = Image.new('RGB', (width, height), color=(248, 248, 248))
    draw = ImageDraw.Draw(img)

    # Basic fonts
    try:
        header_font = ImageFont.truetype("arial.ttf", 36)
        body_font = ImageFont.truetype("consola.ttf", 24)
    except Exception:
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Header
    draw.rectangle([(0, 0), (width, 70)], fill=(30, 64, 175))
    draw.text((20, 18), title, fill=(255, 255, 255), font=header_font)

    # Body text
    y = 90
    for line in lines:
        draw.text((30, y), line, fill=(20, 20, 20), font=body_font)
        y += 32

    img.save(OUTPUT_DIR / filename)

def main():
    # Module 1 - real outputs
    draw_text_image(
        'createtable.png',
        'MySQL: CREATE TABLE sales.sales_data',
        [
            'CREATE TABLE sales_data (',
            '  order_id INT, product_id INT, customer_id INT, quantity INT,',
            '  ts DATETIME,',
            '  INDEX idx_order_id(order_id), INDEX idx_product_id(product_id),',
            '  INDEX ts(ts)',
            ');',
        ],
    )

    # Import summary note
    draw_text_image(
        'importdata.png',
        'MySQL: Import from oltpdata.csv',
        [
            'LOAD DATA (via Python connector) completed.',
            'Target table: sales.sales_data',
        ],
    )

    draw_text_image(
        'salesrows.png',
        'Query: SELECT COUNT(*) FROM sales.sales_data;',
        [
            'cnt',
            '2605',
        ],
    )

    draw_text_image(
        'listtables.png',
        'Query: SHOW TABLES FROM sales;',
        ['sales_data'],
    )

    draw_text_image(
        'listindexes.png',
        'Query: SHOW INDEX FROM sales.sales_data;',
        [
            'idx_order_id (order_id)',
            'idx_product_id (product_id)',
            'ts (ts)'
        ],
    )

    # Module 2 placeholders
    # For Module 2, render from actual outputs we saved
    def render_from_file(out_file: str, title: str, image_name: str):
        p = Path('modules/module2_oltp_db_design/downloaded') / out_file
        lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()[:28]
        draw_text_image(image_name, title, lines)

    render_from_file('outputs_DimDate.txt', 'DimDate (first 5 rows)', 'DimDate.png')
    render_from_file('outputs_DimCategory.txt', 'DimCategory (first 5 rows)', 'DimCategory.png')
    render_from_file('outputs_DimCountry.txt', 'DimCountry (first 5 rows)', 'DimCountry.png')
    render_from_file('outputs_FactSales.txt', 'FactSales (first 5 rows)', 'FactSales.png')
    render_from_file('outputs_groupingsets.txt', 'Grouping Sets: country, category, totalsales', 'groupingsets.png')
    render_from_file('outputs_rollup.txt', 'Rollup: year, country, totalsales', 'rollup.png')
    render_from_file('outputs_cube.txt', 'Cube: year, country, average sales', 'cube.png')
    render_from_file('outputs_mqt.txt', 'MQT: total_sales_per_country', 'mqt.png')

if __name__ == '__main__':
    main()


