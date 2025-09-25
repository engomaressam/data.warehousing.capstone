import pandas as pd
from pathlib import Path

p = Path('modules/module3_staging_dw/downloaded/CustomerLoyaltyProgram.csv')
df = pd.read_csv(p)
# Normalize revenue removing commas
if df['Revenue'].dtype == object:
    df['Revenue'] = df['Revenue'].str.replace(',', '', regex=False)
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)

cat_col = 'Category' if 'Category' in df.columns else 'Product Line'
cats = df.groupby(cat_col)['Revenue'].sum().sort_values(ascending=False)
top_cat = cats.index[0]
bot_cat = cats.index[-1]

min_month = max_month = 'NA'
if 'Month' in df.columns:
    # Prefer 2020 if present, else use all data
    d = df
    if 'Order Year' in df.columns and (df['Order Year'] == 2020).any():
        d = df[df['Order Year'] == 2020]
    monthly = d.groupby('Month')['Revenue'].sum().sort_index()
    if len(monthly) > 0:
        min_month = int(monthly.idxmin())
        max_month = int(monthly.idxmax())

quarter_col = 'Quarter' if 'Quarter' in df.columns else None
min_quarter = 'NA'
if quarter_col:
    mobile_mask = pd.Series([False] * len(df))
    for c in ['Category', 'Product Line']:
        if c in df.columns:
            mobile_mask = mobile_mask | df[c].astype(str).str.contains('Mobile|Phone', case=False, na=False)
    # Map quarters Q1..Q4 to 1..4 for ordering
    def q_to_num(q: str):
        try:
            return int(str(q).strip().upper().replace('Q', ''))
        except Exception:
            return None
    qdf = df[mobile_mask].copy()
    qdf['qnum'] = qdf[quarter_col].map(q_to_num)
    q = qdf.groupby('qnum')['Revenue'].sum()
    if len(q) > 0:
        min_quarter = int(q.idxmin())

print({'top_category': top_cat, 'bottom_category': bot_cat, 'min_month': min_month, 'max_month': max_month, 'min_quarter': min_quarter})

# Additional heuristic answers for required choices
def q_to_num(q: str):
    try:
        return int(str(q).strip().upper().replace('Q', ''))
    except Exception:
        return None

# Month min/max via quarter for 2020
if 'Order Year' in df.columns and 'Quarter' in df.columns:
    d2020 = df[df['Order Year'] == 2020].copy()
    if not d2020.empty:
        d2020['MonthIdx'] = d2020['Quarter'].map(q_to_num)
        monthly = d2020.groupby('MonthIdx')['Revenue'].sum().reindex([1, 2, 3, 4])
        if monthly.notna().any():
            print({'month_min_via_quarter': int(monthly.idxmin()), 'month_max_via_quarter': int(monthly.idxmax())})

# Mobile phones proxy: Smart Electronics or values containing Phone/Mobile
mob_mask = pd.Series([False] * len(df))
if 'Product Line' in df.columns:
    mob_mask = mob_mask | df['Product Line'].astype(str).str.contains('Smart|Phone|Mobile', case=False, na=False)
if 'Category' in df.columns:
    mob_mask = mob_mask | df['Category'].astype(str).str.contains('Phone|Mobile', case=False, na=False)
if mob_mask.any() and 'Quarter' in df.columns:
    qdf = df[mob_mask].copy()
    qdf['qnum'] = qdf['Quarter'].map(q_to_num)
    qs = qdf.groupby('qnum')['Revenue'].sum().reindex([1, 2, 3, 4])
    if qs.notna().any():
        print({'mobile_min_quarter': int(qs.idxmin())})


