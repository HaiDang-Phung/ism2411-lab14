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
# EXERCISE 4: Fix types
print("\n--- EXERCISE 4: FIX TYPES ---")
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
print("Dates converted to NaT:", df["order_date"].isnull().sum())
df["unit_price"] = (
    df["unit_price"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)
df["quantity_sold"] = df["quantity_sold"].astype(int)
df["revenue"] = (df["unit_price"] * df["quantity_sold"]).round(2)
print("\nUpdated dtypes:\n", df.dtypes)
# EXERCISE 5: Check duplicates
print("\n--- EXERCISE 5: CHECK DUPLICATES ---")
duplicate_count = df.duplicated().sum()
print("Duplicate rows found:", duplicate_count)
if duplicate_count > 0:
    df = df.drop_duplicates()
print("Shape after removing duplicates:", df.shape)
# EXERCISE 6: Describe
print("\n--- EXERCISE 6: DESCRIBE ---")
print(df.describe())
"""
Suspicious Statistics & Business Explanations:
1. Extreme maximum in quantity_sold (9,999) and revenue: A single order of 9,999 units pulls the mean far above the median (50%). This is a manual data-entry placeholder or test record rather than a genuine retail purchase.
2. Negative minimums in unit_price and revenue: Negative values represent customer product returns/refunds (money refunded back to customers), which are valid accounting events and must be kept.
"""
# Drop rows where quantity_sold == 9999 because it is an artificial placeholder that distorts sales metrics, while keeping negative revenues as legitimate customer returns.
df = df[df["quantity_sold"] != 9999]
print("Shape after dropping quantity_sold == 9999:", df.shape)
# EXERCISE 7: Save
print("\n--- EXERCISE 7: SAVE ---")
df.to_csv("data/clean_sales.csv", index=False)
df_check_raw = pd.read_csv("data/clean_sales.csv")
print("\nInfo after standard read_csv:")
print(df_check_raw.info())
df_check_parsed = pd.read_csv("data/clean_sales.csv", parse_dates=["order_date"])
print("\nInfo after read_csv with parse_dates=['order_date']:")
print(df_check_parsed.info())