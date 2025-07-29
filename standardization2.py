import pandas as pd

# 读取上一步生成的完整 CSV
df = pd.read_csv('Cleaned_TableC1.csv')

# 找到“Road transport”所在行，截取之前的内容
cutoff_index = df[df.iloc[:, 0].astype(str).str.contains('Road transport', case=False, na=False)].index[0]
df_main = df.iloc[:cutoff_index]

# 将列名恢复为标准字符串并清除空格
df_main.columns = df_main.columns.astype(str).str.strip()

# 重命名第一列为 Sector，第二列为 Fuel（按 C1 表结构）
df_main.rename(columns={df_main.columns[0]: 'Sector', df_main.columns[1]: 'Fuel'}, inplace=True)

# 清理空值
df_main.dropna(subset=['Sector', 'Fuel'], inplace=True)

# 选择数值型年份列
value_vars = [col for col in df_main.columns if col.isdigit()]
df_long = pd.melt(df_main, id_vars=['Sector', 'Fuel'], value_vars=value_vars,
                  var_name='Year', value_name='Consumption_ktoe')

# 去除空值
df_long.dropna(subset=['Consumption_ktoe'], inplace=True)

# 类型转换
df_long['Year'] = df_long['Year'].astype(int)
df_long['Consumption_ktoe'] = pd.to_numeric(df_long['Consumption_ktoe'], errors='coerce')
df_long.dropna(subset=['Consumption_ktoe'], inplace=True)

# 保存为新的清洗后 CSV
df_long.to_csv('Standardized_Industry_Data.csv', index=False)

print(df_long.head())
