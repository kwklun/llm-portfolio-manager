import pandas as pd

# Define the list of useful columns
useful_columns = [
    'date', 'TICKER', 'BIDLO', 'ASKHI', 'PRC', 'VOL', 'RET', 'BID', 'ASK',
    'CFACPR', 'CFACSHR', 'OPENPRC', 'NUMTRD', 'RETX', 'vwretd', 'vwretx',
    'ewretd', 'ewretx', 'sprtrn'
]

# Input and output file paths
input_file = 'sp500.csv'  # Replace with your actual input CSV file path
output_file = 'sp500_filtered.csv'

# Read the CSV file, selecting only the useful columns
# Use low_memory=False to avoid DtypeWarning, as seen in your earlier output
try:
    df = pd.read_csv(input_file, usecols=useful_columns, low_memory=False)
    
    # Convert 'date' to datetime for consistency
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date (optional, but useful for time series)
    df = df.sort_values('date')
    
    # Export the filtered DataFrame to a new CSV
    df.to_csv(output_file, index=False)
    
    print(f"Successfully filtered and exported data to {output_file}")
    print(f"Number of rows: {len(df)}")
    print(f"Columns exported: {list(df.columns)}")
    
    # Optional: Display the first few rows to verify
    print("\nFirst 5 rows of the filtered data:")
    print(df.head())

except FileNotFoundError:
    print(f"Error: The file {input_file} was not found.")
except KeyError as e:
    print(f"Error: One or more specified columns not found in the CSV: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# If you want to test with your sample data instead of a file, uncomment below:
"""
# Sample data for testing
data = '''PERMNO,date,NAMEENDT,SHRCD,EXCHCD,SICCD,NCUSIP,TICKER,COMNAM,SHRCLS,TSYMBOL,NAICS,PRIMEXCH,TRDSTAT,SECSTAT,PERMCO,ISSUNO,HEXCD,HSICCD,CUSIP,DCLRDT,DLAMT,DLPDT,DLSTCD,NEXTDT,PAYDT,RCRDDT,SHRFLG,HSICMG,HSICIG,DISTCD,DIVAMT,FACPR,FACSHR,ACPERM,ACCOMP,SHRENDDT,NWPERM,DLRETX,DLPRC,DLRET,TRTSCD,NMSIND,MMCNT,NSDINX,BIDLO,ASKHI,PRC,VOL,RET,BID,ASK,SHROUT,CFACPR,CFACSHR,OPENPRC,NUMTRD,RETX,vwretd,vwretx,ewretd,ewretx,sprtrn
10104,2019-01-02,,11,1,7372,68389X10,ORCL,ORACLE CORP,,ORCL,511210,N,A,R,8045,10536,1,7379,68389X10,,,,,,,,,,,,,,,,,,,,,,,,,,44.45000,45.34000,45.22000,14320441,0.001550,45.20000,45.21000,3588919,1,1,44.48000,,0.001550,0.001796,0.001791,0.017126,0.017105,0.001269
10104,2019-01-03,,11,1,7372,68389X10,ORCL,ORACLE CORP,,ORCL,511210,N,A,R,8045,10536,1,7379,68389X10,,,,,,,,,,,,,,,,,,,,,,,,,,44.41000,45.50000,44.78000,19868713,-0.009730,44.78000,44.79000,3588919,1,1,44.75000,,-0.009730,-0.021043,-0.021229,-0.009454,-0.009493,-0.024757'''
df = pd.read_csv(pd.compat.StringIO(data), usecols=useful_columns)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')
df.to_csv(output_file, index=False)
print(f"Sample data filtered and exported to {output_file}")
print(df.head())
"""