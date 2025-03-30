import pandas as pd
from sales_pipeline.utils.constants import CLEANED_CSV


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows with NaN values
    df = df.dropna()

    # Remove rows that contain "Order ID" in the Order ID column to remove column titles
    df = df[df["Order ID"] != "Order ID"]

    # Convert data types
    df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"], errors="coerce")
    df["Price Each"] = pd.to_numeric(df["Price Each"], errors="coerce")

    # Optimized datetime parsing by specifying exact format
    datetime_format = "%m/%d/%y %H:%M"
    df["Order Date"] = pd.to_datetime(df["Order Date"], format=datetime_format, errors="coerce")

    # Drop rows with invalid dates
    df = df.dropna(subset=["Order Date"])

    # Add YearMonth column for multi-year support
    df["YearMonth"] = df["Order Date"].dt.to_period("M")

    # Create Month column for optional use
    df["Month"] = df["Order Date"].dt.month

    # Extract City from Purchase Address
    def extract_city(address):
        return address.split(",")[1].strip()

    def extract_state(address):
        return address.split(",")[2].split(" ")[1]

    df["City"] = df["Purchase Address"].apply(lambda x: f"{extract_city(x)} ({extract_state(x)})")

    # Create Sales column for analysis
    df["Sales"] = df["Quantity Ordered"] * df["Price Each"]

    # Save cleaned dataset
    df.to_csv(CLEANED_CSV, index=False)

    return df
