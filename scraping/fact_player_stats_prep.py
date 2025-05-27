import pandas as pd
import os
from pathlib import Path


def merge_csv_files(folder_path='a'):
    """
    Loads all CSV files from the specified folder and merges them into one DataFrame.
    Each subsequent file is added as new rows.

    Args:
        folder_path (str): Path to the folder containing CSV files

    Returns:
        pandas.DataFrame: Merged DataFrame from all CSV files
    """

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist!")
        return None

    # Find all CSV files in the folder
    csv_files = []
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            csv_files.append(os.path.join(folder_path, file))

    if not csv_files:
        print(f"No CSV files found in folder '{folder_path}'")
        return None

    print(f"Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(f"  - {os.path.basename(file)}")

    # List to store DataFrames
    dataframes = []

    # Load each CSV file
    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)
            dataframes.append(df)
            print(f"✓ Loaded {file_path} ({len(df)} rows, {len(df.columns)} columns)")
        except Exception as e:
            print(f"✗ Error loading {file_path}: {e}")

    if not dataframes:
        print("Failed to load any CSV files")
        return None

    # Merge all DataFrames (ignore_index=True resets indices)
    merged_df = pd.concat(dataframes, ignore_index=True, sort=False)

    print(f"\n✓ Successfully merged {len(dataframes)} files")
    print(f"Resulting DataFrame: {len(merged_df)} rows, {len(merged_df.columns)} columns")

    return merged_df


# Main script execution
if __name__ == "__main__":
    # Load and merge CSV files from folder 'a'
    result = merge_csv_files('data_ms')

    if result is not None:
        # Display basic information about the result
        print("\nPreview of first 5 rows:")
        print(result.head())

        print("\nDataFrame info:")
        print(result.info())

        # Optionally: save result to a new CSV file
        output_file = 'match_stats_merged.csv'
        result.to_csv(output_file, index=False)
        print(f"\n✓ Result saved to file: {output_file}")
    else:
        print("Operation failed")