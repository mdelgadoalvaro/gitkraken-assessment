import os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
from fpdf import FPDF
from itertools import combinations
from collections import Counter
from sales_pipeline.utils.logger import get_logger
from sales_pipeline.utils.constants import (
    REPORT_PDF,
    MONTHLY_SALES_IMG,
    CITY_SALES_IMG,
    PRODUCT_SALES_IMG,
    BUNDLING_IMG
)

logger = get_logger("analyze")


def currency_formatter(x, pos):
    return f"${x:,.0f}"


def generate_charts_and_report(df: pd.DataFrame, output_dir: str = "reports") -> None:
    os.makedirs(output_dir, exist_ok=True)

    # Filter only 2019 data
    df = df[df["Order Date"].dt.year == 2019].copy()

    # Use Year-Month for grouping
    df["YearMonth"] = df["Order Date"].dt.to_period("M")
    monthly_sales = df.groupby("YearMonth")["Sales"].sum()
    best_month = monthly_sales.idxmax()
    best_month_sales = monthly_sales.max()
    monthly_sales.index = monthly_sales.index.astype(str)

    plt.figure(figsize=(12, 6))
    plt.bar(monthly_sales.index, monthly_sales.values, color="skyblue")
    plt.xlabel("Month")
    plt.ylabel("Total Sales ($)")
    plt.title("Total Sales by Month")
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    plt.tight_layout()
    plt.savefig(MONTHLY_SALES_IMG, bbox_inches="tight")
    plt.close()

    # Sales by City
    city_sales = df.groupby("City")["Sales"].sum()
    best_city = city_sales.idxmax()
    best_city_sales = city_sales.max()

    plt.figure(figsize=(12, 6))
    plt.bar(city_sales.index, city_sales.values, color="lightcoral")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("City")
    plt.ylabel("Total Sales ($)")
    plt.title("Total Sales by City")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    plt.tight_layout()
    plt.savefig(CITY_SALES_IMG, bbox_inches="tight")
    plt.close()

    # Best-Selling Product
    product_sales = df.groupby("Product")["Quantity Ordered"].sum().sort_values(ascending=False)
    best_product = product_sales.idxmax()
    best_product_sales = product_sales.max()

    plt.figure(figsize=(14, 7))
    plt.bar(product_sales.index, product_sales.values, color="seagreen")
    plt.xticks(rotation=90, ha="right")
    plt.xlabel("Product")
    plt.ylabel("Total Quantity Sold")
    plt.tight_layout()
    plt.savefig(PRODUCT_SALES_IMG, bbox_inches="tight")
    plt.close()

    # Bundling Analysis for AAA Batteries
    multi_orders = df[df["Order ID"].duplicated(keep=False)]
    grouped_orders = multi_orders.groupby("Order ID")["Product"].apply(list)
    pair_counts = Counter()
    for products in grouped_orders:
        pairs = combinations(set(products), 2)
        pair_counts.update(pairs)

    related_aaa = [(pair, count) for pair, count in pair_counts.items() if "AAA Batteries (4-pack)" in pair]
    related_aaa = sorted(related_aaa, key=lambda x: x[1], reverse=True)[:5]
    labels = [pair[0] if pair[1] == "AAA Batteries (4-pack)" else pair[1] for pair, _ in related_aaa]
    values = [count for _, count in related_aaa]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color="orange")
    plt.xlabel("Co-purchased Product")
    plt.ylabel("Frequency")
    plt.title("Most Frequent Bundles with 'AAA Batteries (4-pack)'")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(BUNDLING_IMG, bbox_inches="tight")
    plt.close()

    # Generate PDF Report
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Sales Data Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "1. Monthly Sales Analysis", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"The best month for sales was {best_month} with total revenue of ${best_month_sales:,.2f}.")
    pdf.image(MONTHLY_SALES_IMG, x=20, w=170)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "2. Sales by City", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"The top-performing city was {best_city} with total revenue of ${best_city_sales:,.2f}.")
    pdf.image(CITY_SALES_IMG, x=20, w=170)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "3. Best-Selling Products", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"The most sold product was '{best_product}', with {best_product_sales:,} units sold.")
    pdf.image(PRODUCT_SALES_IMG, x=20, w=170)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "4. Why Did 'AAA Batteries (4-pack)' Sell the Most?", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(
        0,
        10,
        "The product with the highest units sold was 'AAA Batteries (4-pack)'. There are several key reasons:\n"
        "\n- Low price point (~$2-$3), making it ideal for impulse purchases."
        "\n- It's a universally needed item with repeat demand (for remotes, controllers, toys, etc.)."
        "\n- Bundling data shows it's frequently bought alongside electronics and household devices.\n"
    )
    pdf.set_font("Arial", "I", 11)
    pdf.cell(200, 10, "Top Products Frequently Bought with 'AAA Batteries (4-pack)'", ln=True)
    pdf.image(BUNDLING_IMG, x=20, w=170)
    pdf.ln(10)

    pdf.output(REPORT_PDF)
    logger.info(f"Report generated: {REPORT_PDF}")
