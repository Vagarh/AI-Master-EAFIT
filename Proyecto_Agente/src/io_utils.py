import pandas as pd
import csv

def read_any(file):
    if file is None: return None
    name = file.name.lower()
    if name.endswith(".csv"):
        # Read a small portion to sniff the delimiter
        try:
            raw = file.read(4096).decode(errors="ignore")
            dialect = csv.Sniffer().sniff(raw)
            delim = dialect.delimiter
        except Exception:
            delim = ","
        finally:
            # Reset the file pointer to the beginning
            file.seek(0)
        return pd.read_csv(file, delimiter=delim)
    else:
        # For .xls or .xlsx
        return pd.read_excel(file)
