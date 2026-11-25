import pandas as pd
import matplotlib.pyplot as plt

CUSTOMER = "Customer Name"   # change if your column is named differently
ORDER_ID = "Order ID"        # optional, used for order counts

df = pd.read_csv("Superstore_Cleaned.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)

# Per-customer summary
g = df.groupby(CUSTOMER)
customers = g.agg(
    total_sales=("Sales", "sum"),
    total_profit=("Profit", "sum"),
    quantity=("Quantity", "sum"),
    first_order=("Order Date", "min"),
    last_order=("Order Date", "max"),
)
if ORDER_ID in df.columns:
    customers["orders"] = g[ORDER_ID].nunique()
    customers["avg_order_value"] = customers["total_sales"] / customers["orders"]

print("Customers:", len(customers))
print("\nTop 10 by sales:")
print(customers.sort_values("total_sales", ascending=False).head(10))
print("\nLoss-making customers:", (customers["total_profit"] < 0).sum())

# Recency: days since last order
snapshot = df["Order Date"].max()
customers["days_since_last_order"] = (snapshot - customers["last_order"]).dt.days

# Chart 1: top 10 customers by sales
top10 = customers["total_sales"].nlargest(10).sort_values()
plt.figure(figsize=(10, 6))
plt.barh(top10.index, top10.values)
plt.title("Top 10 Customers by Sales")
plt.xlabel("Total Sales")
plt.tight_layout()

# Chart 2: sales vs profit per customer
plt.figure(figsize=(10, 6))
plt.scatter(customers["total_sales"], customers["total_profit"], alpha=0.6)
plt.axhline(0, color="red", linewidth=1)
plt.title("Customer Sales vs Profit")
plt.xlabel("Total Sales")
plt.ylabel("Total Profit")
plt.tight_layout()

customers.to_csv("customer_summary.csv")
plt.show()