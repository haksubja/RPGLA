from polars import LazyFrame, scan_csv
from csv import Error, Sniffer
from pathlib import Path


def _detect_delimiter(file_path: str, sample_size: int = 10000) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        # Read a small sample to analyze
        sample = f.read(sample_size)
        try:
            dialect = Sniffer().sniff(sample, delimiters=[",", ";"])
            return dialect.delimiter
        except Error:
            # Fallback to a default if sniffing fails
            return ","


def GetLazyData(file_path: str) -> LazyFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No data found at {file_path}")

    delimiter = _detect_delimiter(file_path)
    
    return scan_csv(
        file_path, 
        separator=delimiter,
        ignore_errors=True # Useful if some rows are malformed in large PoE dumps
    )