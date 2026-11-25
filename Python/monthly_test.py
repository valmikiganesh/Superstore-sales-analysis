import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Superstore_Cleaned.csv")
print(df.columns.tolist())

df["Order Date"] = pd.to_datetime(df["Order Date"],dayfirst=True)

monthly_sales = df.groupby(
    df["Order Date"].dt.to_period("M")
)["Sales"].sum()

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index.astype(str), monthly_sales.values, marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()