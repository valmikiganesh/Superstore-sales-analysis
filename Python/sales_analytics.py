import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Superstore_Cleaned.csv")

print("FIRST 5 ROWS")
print(df.head())

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nDATA INFORMATION")
df.info()

# Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# Check duplicate rows
print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

# Check data types
print("\nDATA TYPES")
print(df.dtypes)

# Statistical summary
print("\nSTATISTICAL SUMMARY")
print(df.describe())

print("\nTOTAL DUPLICATE ROWS:")
print(df.duplicated().sum())

print("\nTOTAL MISSING VALUES:")
print(df.isnull().sum().sum())

print("\nMISSING VALUES BY COLUMN:")
print(df.isnull().sum())

# Sales by Category

category_sales = df.groupby("Category")["Sales"].sum()

plt.figure(figsize=(9, 5))

category_sales.plot(
    kind="bar",
    title="Sales by Category"
)

plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Convert Order Date to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Monthly sales analysis
df["Year_Month"] = df["Order_Date"].dt.to_period("M")

monthly_sales = df.groupby("Year_Month")["Sales"].sum()

# Create line chart
plt.figure(figsize=(12, 6))

monthly_sales.plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# TEST MONTHLY SALES CHART

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

monthly_sales = df.groupby(
    df["Order_Date"].dt.to_period("M")
)["Sales"].sum()

print(monthly_sales)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index.astype(str),
         monthly_sales.values, marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()

plt.savefig("monthly_sales.png")
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Superstore_Cleaned.csv")
print(df.columns.tolist())

df["Order Date"] = pd.to_datetime(df["Order Date"])

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

import pandas as pd

df = pd.read_csv("Superstore_Cleaned.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

# Core KPIs
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()
total_quantity = df["Quantity"].sum()

profit_margin = total_profit / total_sales * 100
avg_order_value = total_sales / total_orders
avg_discount = df["Discount"].mean() * 100
orders_per_customer = total_orders / total_customers
avg_ship_days = (df["Ship Date"] - df["Order Date"]).dt.days.mean()

# Loss-making share
loss_rows = (df["Profit"] < 0).mean() * 100

print("===== KEY BUSINESS KPIs =====")
print(f"Total Sales:          {total_sales:,.2f}")
print(f"Total Profit:         {total_profit:,.2f}")
print(f"Profit Margin:        {profit_margin:.2f}%")
print(f"Total Orders:         {total_orders:,}")
print(f"Total Customers:      {total_customers:,}")
print(f"Total Quantity Sold:  {total_quantity:,}")
print(f"Avg Order Value:      {avg_order_value:,.2f}")
print(f"Orders per Customer:  {orders_per_customer:.2f}")
print(f"Avg Discount:         {avg_discount:.2f}%")
print(f"Avg Shipping Days:    {avg_ship_days:.2f}")
print(f"Loss-making lines:    {loss_rows:.2f}%")

# KPIs by dimension
def kpi_by(col):
    t = df.groupby(col).agg(
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        orders=("Order ID", "nunique"),
    )
    t["margin_%"] = t["profit"] / t["sales"] * 100
    return t.sort_values("sales", ascending=False).round(2)

for col in ["Category", "Region", "Segment"]:
    print(f"\n--- KPIs by {col} ---")
    print(kpi_by(col))

print("\n--- Top 5 Sub-Categories by Profit ---")
print(kpi_by("Sub-Category").sort_values("profit", ascending=False).head(5))

print("\n--- Bottom 5 Sub-Categories by Profit ---")
print(kpi_by("Sub-Category").sort_values("profit").head(5))

# Year-over-year growth
yearly = df.groupby(df["Order Date"].dt.year)[["Sales", "Profit"]].sum()
yearly["sales_growth_%"] = yearly["Sales"].pct_change() * 100
print("\n--- Yearly Sales and Growth ---")
print(yearly.round(2))