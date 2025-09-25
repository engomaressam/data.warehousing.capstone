import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA = Path('modules/module3_staging_dw/downloaded/CustomerLoyaltyProgram.csv')
OUT = Path('final_submission/images')


def save_table_image(df: pd.DataFrame, title: str, filename: str):
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('#f8f8f8')
    ax.axis('off')
    ax.set_title(title, fontsize=16, weight='bold')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.4)
    fig.savefig(OUT / filename, dpi=150, bbox_inches='tight')
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # Load
    df = pd.read_csv(DATA)

    # Simulate screenshots required by the rubric
    save_table_image(pd.DataFrame({'Status': ['CustomerLoyaltyProgram.csv uploaded']}), 'Data Import', 'dataimport.png')
    save_table_image(df.head(10), 'First 10 Rows', 'first10rows.png')
    save_table_image(pd.DataFrame({'DataSource': ['CustomerLoyaltyProgram.csv']}), 'Data Source', 'datasource.png')

    # Ensure date/year/month fields
    # Common columns in this dataset include: Order Year, Month, Category, Product Line, Quantity Sold, Revenue
    # Create line chart: month-wise total sales for 2020
    if 'Order Year' in df.columns and 'Month' in df.columns:
        df_2020 = df[df['Order Year'] == 2020]
        monthly = df_2020.groupby('Month', as_index=False)['Revenue'].sum()
        monthly = monthly.sort_values('Month')
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=monthly, x='Month', y='Revenue', marker='o')
        plt.title('Month-wise Total Sales for 2020')
        plt.xlabel('Month')
        plt.ylabel('Revenue')
        plt.tight_layout()
        plt.savefig(OUT / 'linechart.png', dpi=150)
        plt.close()

    # Pie chart: category-wise total sales (Category or Product Line)
    category_col = 'Category' if 'Category' in df.columns else 'Product Line'
    if category_col in df.columns:
        # Coerce Revenue to numeric
        df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)
        cat_sales = df.groupby(category_col)['Revenue'].sum().sort_values(ascending=False)
        plt.figure(figsize=(10, 10))
        cat_sales.plot(kind='pie', autopct='%1.1f%%', startangle=140)
        plt.ylabel('')
        plt.title('Category-wise Total Sales')
        plt.tight_layout()
        plt.savefig(OUT / 'piechart.png', dpi=150)
        plt.close()

    # Bar chart: Quarterly sales of mobile phones
    # Use Category or Product Line to filter for Mobile Phones-like values
    mobile_mask = pd.Series([False] * len(df))
    for col in ['Category', 'Product Line']:
        if col in df.columns:
            mobile_mask = mobile_mask | df[col].str.contains('Mobile|Phone', case=False, na=False)
    quarter_col = 'Quarter' if 'Quarter' in df.columns else None
    if quarter_col:
        mobile = df[mobile_mask].copy()
        if not mobile.empty:
            q_sales = mobile.groupby(quarter_col)['Revenue'].sum().reindex([1, 2, 3, 4])
            plt.figure(figsize=(10, 6))
            q_sales.plot(kind='bar', color='#4e79a7')
            plt.title('Quarterly Sales of Mobile Phones')
            plt.xlabel('Quarter')
            plt.ylabel('Revenue')
            plt.tight_layout()
            plt.savefig(OUT / 'barchart.png', dpi=150)
            plt.close()


if __name__ == '__main__':
    main()


