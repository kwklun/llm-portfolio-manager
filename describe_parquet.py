import pandas as pd
import pyarrow.parquet as pq
import os

# Specify the folder path containing the .parquet files
folder_path = "/Users/kwklun/llm-portfolio-manager/data_mfin_7037_2024"

# List of .parquet files to process
parquet_files = [
    "comp.finratios.parquet",
    "comp.funda.parquet",
    "crsp.ccmxpf_linktable.parquet",
    "crsp.dsenames.parquet",
    "crsp.dsf.parquet",
    "crsp.msedelist.parquet",
    "crsp.msf_delisting_adjusted.parquet",
    "crsp.msf.parquet"
]

# Output file
output_file = "parquet_desc.txt"

# Open the output file in write mode
with open(output_file, "w") as f:
    # Loop through each .parquet file
    for file_name in parquet_files:
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            f.write(f"\n{'='*50}\n")
            f.write(f"File not found: {file_path}\n")
            f.write(f"{'='*50}\n")
            continue
        
        # Write header for the file
        f.write(f"\n{'='*50}\n")
        f.write(f"Processing file: {file_name}\n")
        f.write(f"{'='*50}\n")

        # 1. Extract Schema using pyarrow (field names and data types)
        try:
            parquet_file = pq.ParquetFile(file_path)
            schema = parquet_file.schema
            f.write("\nField Names and Data Types:\n")
            f.write(str(schema) + "\n")
        except Exception as e:
            f.write(f"Error reading schema: {e}\n")

        # 2. Load Data into Pandas and Show First 5 Rows
        try:
            df = pd.read_parquet(file_path)
            f.write("\nFirst 5 Rows:\n")
            f.write(df.head().to_string() + "\n")
        except Exception as e:
            f.write(f"Error processing data: {e}\n")

print(f"Output written to {output_file}")