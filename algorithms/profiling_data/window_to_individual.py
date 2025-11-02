import pandas as pd
import os

# =====================================================================================
# Configuration Area
# =====================================================================================
# Define the input and output file paths here.
# These are the only values you should need to change.

# Path to the source file containing windowed merge results.
INPUT_CSV_PATH = "./window_merge.csv"

# Path where the new file for individual layer results will be saved.
OUTPUT_CSV_PATH = "./individual_layer_merge.csv"

# =====================================================================================


def generate_individual_from_window(input_file: str, output_file: str):
    """
    Reads a window_merge.csv file, filters for single-layer merges (window_size=1),
    and creates a corresponding individual_layer_merge.csv file.

    Args:
        input_file (str): Path to the source window_merge.csv file.
        output_file (str): Path for the destination individual_layer_merge.csv file.
    """
    print("--- Starting data generation ---")

    # 1. Check if the input file exists.
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at '{input_file}'")
        return

    print(f"1. Reading data from '{input_file}'...")
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    # 2. Filter the DataFrame to include only rows where window_size is 1.
    print("2. Filtering for rows where window_size == 1...")
    df_individual = df[df['window_size'] == 1].copy()

    if df_individual.empty:
        print("Warning: No rows with window_size == 1 were found in the input file.")
        return

    # 3. Rename columns to match the format required by run_heuristic.py.
    #    'start_layer' -> 'layer_id'
    #    'base_type'   -> 'base_model'
    print("3. Renaming columns...")
    df_individual.rename(columns={
        'start_layer': 'layer_id',
        'base_type': 'base_model'
    }, inplace=True)

    # 4. Select and reorder the final columns, dropping the now-unnecessary ones.
    final_columns = ['layer_id', 'base_model', 'metric', 'accuracy']
    try:
        final_df = df_individual[final_columns]
    except KeyError as e:
        print(f"Error: The input file is missing a required column: {e}.")
        print(f"Please ensure the file contains all of the following: {final_columns}")
        return

    # 5. Save the transformed DataFrame to the output CSV file.
    print(f"4. Saving results to '{output_file}'...")
    try:
        final_df.to_csv(output_file, index=False)
        print(f"--- Success! File has been generated. ---")
    except Exception as e:
        print(f"Error saving the output file: {e}")


def main():
    """Main execution function."""
    # Ensure the output directory exists before trying to save the file.
    output_dir = os.path.dirname(OUTPUT_CSV_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    generate_individual_from_window(INPUT_CSV_PATH, OUTPUT_CSV_PATH)


if __name__ == '__main__':
    main()