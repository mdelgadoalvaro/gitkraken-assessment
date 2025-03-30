import os
import pandas as pd


def explore_data(data_folder: str = './data'):
    print("Exploring dataset...\n")

    # List all CSV files
    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
    print(f"Found {len(csv_files)} CSV files.")
    for file in csv_files:
        print(f" - {file}")

    # Load all files into one DataFrame
    all_data = pd.DataFrame()
    for file in csv_files:
        df = pd.read_csv(os.path.join(data_folder, file))
        print(f"\nInspecting: {file}")
        print(f"Shape: {df.shape}")
        print("Columns:", df.columns.tolist())
        print("Sample rows:")
        print(df.head(2))

        # Check for nulls
        print("\nNull values per column:")
        print(df.isnull().sum())

        # Check data types
        print("\nData types:")
        print(df.dtypes)

        # Convert to columns to numeric
        numeric_columns = ["Quantity Ordered", "Price Each", "Order ID"]  # if applicable
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Check if 'Order ID' or any other field has strange non-numeric values
        if 'Order ID' in df.columns:
            order_ids = df['Order ID'].astype(str)
            non_numeric_ids = df[~order_ids.str.isnumeric() & df['Order ID'].notna()]
            if not non_numeric_ids.empty:
                print(f"Found {len(non_numeric_ids)} non-numeric Order IDs (possibly header rows mixed in).")

        all_data = pd.concat([all_data, df], ignore_index=True)

    print("\nCombined Dataset Summary:")
    print(all_data.describe())
    print("\nTotal nulls in combined dataset:")
    print(all_data.isnull().sum())

    # Additional insight: Check range of years in the data
    datetime_format = "%m/%d/%y %H:%M"
    all_data['Order Date'] = pd.to_datetime(all_data['Order Date'], format=datetime_format, errors='coerce')
    years = all_data['Order Date'].dt.year.dropna().astype(int).unique()
    years_str = ", ".join(str(y) for y in sorted(years))
    print("\nData includes records from the following years:", years_str)

    # Print months and counts per year
    print("\nRecord count per year and month:")
    year_month_counts = all_data['Order Date'].dt.to_period('M').value_counts().sort_index()
    for ym, count in year_month_counts.items():
        print(f"  {ym}: {count} records")


if __name__ == '__main__':
    explore_data()
