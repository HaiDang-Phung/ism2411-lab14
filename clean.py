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
# EXERCISE 2: Standardize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")
print("\n--- EXERCISE 2: UPDATED COLUMNS ---")
print(df.columns.tolist())
# EXERCISE 3: Handle missing values
print("\n--- EXERCISE 3: HANDLE MISSING VALUES ---")
print("Shape before:", df.shape)
# Fill missing values in numeric column 'quantity_sold' with the column mean
# Why: Only 1.96% of rows are missing quantity, so imputing with the mean preserves valid sales records without distorting overall volume.
df["quantity_sold"] = df["quantity_sold"].fillna(df["quantity_sold"].mean())
# Drop rows missing essential identifiers ('order_id' or 'order_date')
# Why: Transactions without a valid ID or date cannot be tracked or analyzed chronologically, so imputing them would create fabricated records.
df = df.dropna(subset=["order_id", "order_date"])
print("Shape after:", df.shape)
print("Missing values after cleaning:\n", df.isnull().sum())