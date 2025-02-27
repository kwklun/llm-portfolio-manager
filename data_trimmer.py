import os
import pandas as pd

FOLDER = "data_mfin_7037_2024/"
OUTPUT_FOLDER = "data_trimmed/"

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# List of your Parquet files
files = [
    FOLDER + 'comp.finratios.parquet',
    FOLDER + 'comp.funda.parquet',
    FOLDER + 'crsp.dsf.parquet',
    FOLDER + 'crsp.msf_delisting_adjusted.parquet',
    FOLDER + 'crsp.msf.parquet'
]

# Target size: ~80MB (adjust N based on trial)
# Start with a reasonable guess, e.g., 100,000 rows, then tweak
N = 100000

for file in files:
    try:
        # Read only the first N rows
        df = pd.read_parquet(file, engine='pyarrow').head(N)
        
        # Generate the new file path inside the output folder
        output_file = os.path.join(OUTPUT_FOLDER, os.path.basename(file).replace('.parquet', '_small.parquet'))
        
        # Save the new file
        df.to_parquet(output_file, engine='pyarrow', compression='snappy')
        
        # Check the size of the new file (in MB)
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"Saved {output_file}: {size_mb:.2f} MB")
        
        # If size isn’t close to 80MB, print a warning
        if size_mb > 90 or size_mb < 70:
            print(f"Warning: {output_file} is {size_mb:.2f} MB, not ~80MB. Adjust N.")
    except Exception as e:
        print(f"Error processing {file}: {e}")