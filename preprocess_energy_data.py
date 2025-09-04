import pandas as pd

# 1. specify rows 5 and 6 as multi-level headers
df_raw = pd.read_excel("TableC2023.xlsx", header=[4, 5])

# 2. Delete empty rows and columns
df_raw.dropna(axis=0, how='all', inplace=True)
df_raw.dropna(axis=1, how='all', inplace=True)

# 3. Rename columns to "Sector_Fuel"
df_raw.columns = [f"{str(c1).strip()}_{str(c2).strip()}" for c1, c2 in df_raw.columns]

# 4. MultiIndex to extract sector and fuel information
df_raw.columns = pd.MultiIndex.from_tuples(
    [tuple(col.split("_", 1)) for col in df_raw.columns]
)

# 5. Extract all sector-fuel data and combine them into long format
data = []
for sector, fuel in df_raw.columns:
    if fuel == 'Year':
        continue  # ignore the Year column within each region
    year_series = df_raw[(sector, 'Year')] if (sector, 'Year') in df_raw.columns else None
    if year_series is None:
        continue
    for year, consumption in zip(year_series, df_raw[(sector, fuel)]):
        if pd.isna(year) or pd.isna(consumption):
            continue  # Skip missing values
        data.append([int(year), sector.strip(), fuel.strip(), consumption])

# 6. Normalized DataFrame
df_long = pd.DataFrame(data, columns=['Year', 'Sector', 'Fuel', 'Consumption_ktoe'])

# 7. Export to CSV
df_long.to_csv("Standardized_Energy_Data.csv", index=False)

# 8. Print Preview
print("Data cleaning completed, first 5 rows example:")
print(df_long.head())
