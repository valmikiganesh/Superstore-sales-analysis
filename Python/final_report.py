import os
import base64
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Load and prepare ----------
df = pd.read_csv("Superstore_Cleaned.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

OUT = "report"
os.makedirs(OUT, exist_ok=True)

# ---------- KPIs ----------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()

kpis = {
    "Total Sales": f"{total_sales:,.0f}",
    "Total Profit": f"{total_profit:,.0f}",
    "Profit Margin": f"{total_profit / total_sales * 100:.2f}%",
    "Orders": f"{total_orders:,}",
    "Customers": f"{total_customers:,}",
    "Avg Order Value": f"{total_sales / total_orders:,.2f}",
    "Avg Discount": f"{df['Discount'].mean() * 100:.2f}%",
    "Avg Ship Days": f"{(df['Ship Date'] - df['Order Date']).dt.days.mean():.1f}",
}

# ---------- Summary tables ----------
def summary(col):
    t = df.groupby(col).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
    )
    t["Margin %"] = t["Profit"] / t["Sales"] * 100
    return t.sort_values("Sales", ascending=False).round(2)

by_category = summary("Category")
by_region = summary("Region")
by_segment = summary("Segment")
by_subcat = summary("Sub-Category")
top_customers = summary("Customer Name").head(10)

yearly = df.groupby(df["Order Date"].dt.year)[["Sales", "Profit"]].sum()
yearly["Sales Growth %"] = yearly["Sales"].pct_change() * 100
yearly = yearly.round(2)

monthly = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()

# ---------- Charts ----------
charts = []

def save_chart(name, title):
    plt.title(title)
    plt.tight_layout()
    path = os.path.join(OUT, name)
    plt.savefig(path, dpi=120)
    plt.close()
    charts.append((title, path))

plt.figure(figsize=(12, 5))
plt.plot(monthly.index.astype(str), monthly.values, marker="o")
plt.xticks(range(0, len(monthly), 3), monthly.index.astype(str)[::3], rotation=45)
plt.grid(True)
save_chart("monthly_sales.png", "Monthly Sales Trend")

plt.figure(figsize=(8, 5))
by_category["Sales"].plot(kind="bar")
plt.xticks(rotation=0)
save_chart("sales_by_category.png", "Sales by Category")

plt.figure(figsize=(8, 5))
by_region["Sales"].plot(kind="bar", color="seagreen")
plt.xticks(rotation=0)
save_chart("sales_by_region.png", "Sales by Region")

plt.figure(figsize=(8, 5))
by_category["Profit"].plot(kind="bar", color="darkorange")
plt.xticks(rotation=0)
save_chart("profit_by_category.png", "Profit by Category")

plt.figure(figsize=(10, 6))
top_customers["Sales"].sort_values().plot(kind="barh", color="purple")
save_chart("top_customers.png", "Top 10 Customers by Sales")

plt.figure(figsize=(10, 6))
by_subcat["Profit"].sort_values().plot(kind="barh", color="teal")
save_chart("profit_by_subcategory.png", "Profit by Sub-Category")

# ---------- Key insights (auto-generated) ----------
best_cat = by_category["Sales"].idxmax()
best_region = by_region["Sales"].idxmax()
worst_sub = by_subcat["Profit"].idxmin()
best_sub = by_subcat["Profit"].idxmax()
loss_subs = (by_subcat["Profit"] < 0).sum()

insights = [
    f"{best_cat} is the top category by sales.",
    f"{best_region} is the top region by sales.",
    f"{best_sub} is the most profitable sub-category; {worst_sub} is the least profitable.",
    f"{loss_subs} sub-categories are loss-making overall.",
    f"Overall profit margin is {kpis['Profit Margin']} on average discount of {kpis['Avg Discount']}.",
]

# ---------- HTML report ----------
def img_tag(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/png;base64,{data}" style="max-width:100%;">'

cards = "".join(
    f'<div class="card"><div class="v">{v}</div><div class="k">{k}</div></div>'
    for k, v in kpis.items()
)
charts_html = "".join(f"<h3>{t}</h3>{img_tag(p)}" for t, p in charts)
insights_html = "".join(f"<li>{i}</li>" for i in insights)

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Superstore Sales Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 30px; color: #222; }}
h1 {{ border-bottom: 3px solid #1f77b4; padding-bottom: 8px; }}
.cards {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.card {{ background: #f2f6fa; border-radius: 8px; padding: 14px 20px; min-width: 150px; }}
.v {{ font-size: 22px; font-weight: bold; color: #1f77b4; }}
.k {{ font-size: 13px; color: #555; }}
table {{ border-collapse: collapse; margin-bottom: 20px; }}
th, td {{ border: 1px solid #ccc; padding: 6px 12px; text-align: right; }}
th {{ background: #1f77b4; color: white; }}
</style></head><body>
<h1>Superstore Sales Report</h1>
<p>Period: {df['Order Date'].min():%d %b %Y} to {df['Order Date'].max():%d %b %Y}</p>

<h2>Key KPIs</h2><div class="cards">{cards}</div>

<h2>Key Insights</h2><ul>{insights_html}</ul>

<h2>Charts</h2>{charts_html}

<h2>Yearly Performance</h2>{yearly.to_html()}
<h2>By Category</h2>{by_category.to_html()}
<h2>By Region</h2>{by_region.to_html()}
<h2>By Segment</h2>{by_segment.to_html()}
<h2>By Sub-Category</h2>{by_subcat.to_html()}
<h2>Top 10 Customers</h2>{top_customers.to_html()}
</body></html>"""

with open(os.path.join(OUT, "final_report.html"), "w", encoding="utf-8") as f:
    f.write(html)

# ---------- Excel export (optional) ----------
try:
    with pd.ExcelWriter(os.path.join(OUT, "final_report.xlsx")) as xl:
        pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"]).to_excel(xl, "KPIs", index=False)
        yearly.to_excel(xl, "Yearly")
        by_category.to_excel(xl, "Category")
        by_region.to_excel(xl, "Region")
        by_segment.to_excel(xl, "Segment")
        by_subcat.to_excel(xl, "SubCategory")
        top_customers.to_excel(xl, "Top Customers")
    print("Excel report saved.")
except ImportError:
    print("Skipped Excel export. Run: pip install openpyxl")

print("\n===== KPIs =====")
for k, v in kpis.items():
    print(f"{k:18}{v}")
print("\n===== Insights =====")
for i in insights:
    print("-", i)
print(f"\nReport saved in the '{OUT}' folder. Open report/final_report.html in your browser.")