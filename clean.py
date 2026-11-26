import pandas as pd
# EXERCISE 1: Inspect
df = pd.read_csv("data/messy_sales.csv")
print("--- EXERCISE 1: INSPECT ---")
print(df.info())
print("\nMissing values per column:\n", df.isnull().sum())
"""
Data Quality Issues Observed:
1. Unit Price is stored as string (str/object) because of '$' signs and commas (e.g., '$38.99'), instead of float64.
2. Order Date is stored as string (str/object) rather than datetime64.
3. Missing values exist across multiple columns: Customer ID has 362 missing (7.54%), Region has 111 missing (2.31%), Quantity Sold has 94 missing (1.96%), Order ID has 31 missing (0.65%), and Order Date has 25 missing (0.52%).
4. Quantity Sold is stored as float64 due to missing NaN values, but should be integer (int64) once cleaned.
"""