import pandas as pd
from pathlib import Path
p = Path('modules/module3_staging_dw/downloaded/CustomerLoyaltyProgram.csv')
df = pd.read_csv(p)
print(list(df.columns))
if 'Order Year' in df.columns:
    print('years', sorted(df['Order Year'].unique().tolist()))
if 'Month' in df.columns:
    print('months', sorted(pd.Series(df['Month'].dropna().unique()).tolist()))
if 'Quarter' in df.columns:
    print('quarters', sorted(pd.Series(df['Quarter'].dropna().unique()).tolist()))

