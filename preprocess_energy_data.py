import pandas as pd

# 1. 加载 TableC1.xlsx，指定第5行和第6行为多级表头
df_raw = pd.read_excel("TableC2023.xlsx", header=[4, 5])

# 2. 删除空行与空列
df_raw.dropna(axis=0, how='all', inplace=True)
df_raw.dropna(axis=1, how='all', inplace=True)

# 3. 重命名列名格式为 "Sector_Fuel"
df_raw.columns = [f"{str(c1).strip()}_{str(c2).strip()}" for c1, c2 in df_raw.columns]

# 4. 构造 MultiIndex 来提取 sector 和 fuel 信息
df_raw.columns = pd.MultiIndex.from_tuples(
    [tuple(col.split("_", 1)) for col in df_raw.columns]
)

# 5. 提取所有 sector-fuel 数据，整合为长格式
data = []
for sector, fuel in df_raw.columns:
    if fuel == 'Year':
        continue  # 忽略各区域内部的 Year 列
    year_series = df_raw[(sector, 'Year')] if (sector, 'Year') in df_raw.columns else None
    if year_series is None:
        continue
    for year, consumption in zip(year_series, df_raw[(sector, fuel)]):
        if pd.isna(year) or pd.isna(consumption):
            continue  # 跳过缺失值
        data.append([int(year), sector.strip(), fuel.strip(), consumption])

# 6. 构建标准化 DataFrame
df_long = pd.DataFrame(data, columns=['Year', 'Sector', 'Fuel', 'Consumption_ktoe'])

# 7. 导出为 CSV
df_long.to_csv("Standardized_Energy_Data.csv", index=False)

# 8. 打印预览
print("✅ 数据清洗完成，前5行示例：")
print(df_long.head())
