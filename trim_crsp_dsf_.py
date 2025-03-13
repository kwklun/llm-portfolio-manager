import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
import os

# Define file paths
input_folder = "data_mfin_7037_2024"
output_folder = "data_trimmed"
dsf_file = os.path.join(input_folder, "crsp.dsf.parquet")
dsenames_file = os.path.join(input_folder, "crsp.dsenames.parquet")
output_file = os.path.join(output_folder, "crsp.dsf_trimmed_with_ticker.parquet")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Fields to keep
dsf_fields = ["date", "permno", "prc", "ret", "vol", "cfacpr", "cfacshr"]
dsenames_fields = ["permno", "namedt", "nameendt", "ticker"]
final_fields = ["date", "ticker", "prc", "ret", "vol", "cfacpr", "cfacshr"]

# Function to process chunks and write incrementally
def process_chunk(dsf_chunk, dsenames_df, writer=None):
    # Convert date to datetime in chunk
    dsf_chunk["date"] = pd.to_datetime(dsf_chunk["date"])

    # Merge with dsenames_df
    merged_chunk = dsf_chunk.merge(dsenames_df, on="permno", how="left")

    # Filter rows where date is within namedt and nameendt
    merged_chunk = merged_chunk[
        (merged_chunk["date"] >= merged_chunk["namedt"]) &
        (merged_chunk["date"] <= merged_chunk["nameendt"])
    ]

    # Select only the final fields
    trimmed_chunk = merged_chunk[final_fields]

    # Convert to PyArrow table
    trimmed_table = pa.Table.from_pandas(trimmed_chunk)

    # Write to file (append if writer exists)
    if writer is None:
        writer = pq.ParquetWriter(output_file, trimmed_table.schema, compression="snappy")
    writer.write_table(trimmed_table)
    return writer

# Load and pre-filter dsenames_df once (assumes it fits in memory)
dsenames_table = pq.read_table(dsenames_file, columns=dsenames_fields)
dsenames_df = dsenames_table.to_pandas()
dsenames_df["namedt"] = pd.to_datetime(dsenames_df["namedt"])
dsenames_df["nameendt"] = pd.to_datetime(dsenames_df["nameendt"]).fillna(pd.Timestamp("2100-01-01"))

# Process dsf in smaller chunks using batching
writer = None
dsf_dataset = pq.ParquetDataset(dsf_file, use_legacy_dataset=False)
batch_size = 100_000  # Adjust this based on your RAM (rows per batch)

for fragment in dsf_dataset.fragments:
    dsf_table = fragment.to_table(columns=dsf_fields)
    dsf_df = dsf_table.to_pandas()

    # Process in smaller batches
    for start in range(0, len(dsf_df), batch_size):
        dsf_chunk = dsf_df.iloc[start:start + batch_size]
        writer = process_chunk(dsf_chunk, dsenames_df, writer)

# Close the writer
if writer:
    writer.close()

# Inspect the result (optional)
trimmed_table = pq.read_table(output_file)
print("Trimmed Schema:")
print(trimmed_table.schema)
print("\nFirst 5 Rows:")
print(trimmed_table.to_pandas().head())

print(f"Trimmed data exported to {output_file}")