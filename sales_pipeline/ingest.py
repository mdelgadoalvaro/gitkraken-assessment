import os
import pandas as pd


def ingest_csvs(path: str) -> pd.DataFrame:
    # Get list of all CSV files
    data_files = [f for f in os.listdir(path) if f.endswith(".csv")]

    # Merge all the CSVs into one DataFrame
    all_data = pd.DataFrame()

    for file in data_files:
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path)
        all_data = pd.concat([all_data, df], ignore_index=True)

    return all_data
