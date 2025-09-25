import pandas as pd
from pathlib import Path

p = Path('modules/module3_staging_dw/downloaded/CustomerLoyaltyProgram.csv')
df = pd.read_csv(p)
if df['Revenue'].dtype == object:
    df['Revenue'] = df['Revenue'].str.replace(',', '', regex=False)
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)

def q_to_num(q: str):
    try:
        return int(str(q).strip().upper().replace('Q', ''))
    except Exception:
        return None

d2020 = df[df['Order Year'] == 2020].copy()
d2020['qnum'] = d2020['Quarter'].map(q_to_num)
qs = d2020.groupby('qnum')['Revenue'].sum().reindex([1, 2, 3, 4])
print('Q sums 2020:', qs.to_dict())
print('min quarter:', int(qs.idxmin()))
print('max quarter:', int(qs.idxmax()))


