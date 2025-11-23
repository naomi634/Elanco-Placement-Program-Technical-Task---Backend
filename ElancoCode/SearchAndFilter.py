# SearchAndFilter.py
import argparse
import logging
from pathlib import Path
import sys

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas is required. Install with: pip install pandas")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_csv(path):
    """
    Load CSV into pandas DataFrame and parse 'date' column to datetime if present.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    # Read everything as string first so we can robustly parse date
    df = pd.read_csv(path, dtype=str)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def filter_by_time_range(df, start=None, end=None):
    """
    Filter dataframe by inclusive start/end datetimes.
    start/end may be ISO strings or any format parsed by pandas.to_datetime.
    """
    if start is None and end is None:
        return df
    if "date" not in df.columns:
        raise KeyError("Cannot filter by time: 'date' column not present")
    res = df.copy()
    if start:
        start_ts = pd.to_datetime(start)
        res = res[res["date"] >= start_ts]
    if end:
        end_ts = pd.to_datetime(end)
        res = res[res["date"] <= end_ts]
    return res


def filter_by_location(df, location=None, match="contains"):
    """
    Filter by location.
    match: 'exact', 'contains', 'starts'
    """
    if location is None or str(location).strip() == "":
        return df
    if "location" not in df.columns:
        raise KeyError("Cannot filter by location: 'location' column not present")
    loc = str(location).strip().lower()
    col = df["location"].fillna("").astype(str).str.lower()
    if match == "exact":
        return df[col == loc]
    if match == "starts":
        return df[col.str.startswith(loc, na=False)]
    # default 'contains'
    return df[col.str.contains(loc, na=False)]


def search(csv_path="cleaned_tick_sightings.csv", start=None, end=None, location=None, match="contains"):
    """
    Load CSV and apply filters. Returns a pandas DataFrame.
    """
    df = load_csv(csv_path)
    df = filter_by_time_range(df, start, end)
    df = filter_by_location(df, location, match)
    return df


def _parse_args(argv=None):
    p = argparse.ArgumentParser(description="Search and filter tick sightings CSV by time range and location")
    p.add_argument("--csv", default="cleaned_tick_sightings.csv", help="Path to cleaned CSV")
    p.add_argument("--start", help="Start datetime (inclusive). ISO or any pandas-parsable format")
    p.add_argument("--end", help="End datetime (inclusive). ISO or any pandas-parsable format")
    p.add_argument("--location", help="Location to filter by (city or text)")
    p.add_argument("--match", choices=["exact", "contains", "starts"], default="contains", help="Location match mode")
    p.add_argument("-o", "--output", help="Write filtered results to CSV")
    p.add_argument("--head", type=int, default=10, help="Print first N rows to stdout when not writing output")
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    try:
        df = search(csv_path=args.csv, start=args.start, end=args.end, location=args.location, match=args.match)
    except Exception as e:
        logging.error("Search failed: %s", e)
        sys.exit(1)

    if args.output:
        out = Path(args.output)
        df.to_csv(out, index=False, encoding="utf-8")
        logging.info("Wrote %d rows to %s", len(df), out)
    else:
        if df.empty:
            logging.info("No results matched the filters")
        else:
            # print head
            print(df.head(args.head).to_string(index=False))
            logging.info("Total matches: %d", len(df))


if __name__ == "__main__":
    main()