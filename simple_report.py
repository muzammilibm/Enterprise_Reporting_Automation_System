import pandas as pd
import datetime as datetime

# read the file
df=pd.read_csv("data/input/512-sample.txt")
print(f"Loaded {len(df)} rows")

# calculate
total = df['count'].sum()
print(f"Total count: {total}")
