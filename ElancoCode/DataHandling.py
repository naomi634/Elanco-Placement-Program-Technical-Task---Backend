# DataHandling.py
import argparse
import logging
from pathlib import Path
import sys

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas and openpyxl are required. Install with: pip install pandas openpyxl")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def clean_data(input_path, output_path=None, sheet_name="Sheet1", preview=False):
    """
    Read Excel -> clean -> write CSV.
    - Drops exact duplicate rows
    - Replaces missing values with "Unknown"
    - Normalises 'date' column to ISO 8601 (YYYY-MM-DDTHH:MM:SS) where possible
    Returns a dict with summary metrics.
    """
    input_path = Path(input_path)
    if output_path:
        output_path = Path(output_path)
    else:
        output_path = input_path.parent / "cleaned_tick_sightings.csv"

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    logging.info("Reading Excel: %s (sheet=%s)", input_path, sheet_name)
    df = pd.read_excel(input_path, sheet_name=sheet_name, engine="openpyxl")

    logging.info("Initial rows: %d", len(df))
    original_rows = len(df)

    # Drop exact duplicate rows
    df = df.drop_duplicates(keep="first")
    duplicates_removed = original_rows - len(df)
    logging.info("Exact duplicate rows removed: %d", duplicates_removed)

    # Replace missing values with 'Unknown'
    df = df.fillna("Unknown")

    # Normalize 'date' column if present
    if "date" in df.columns:
        logging.info("Normalising 'date' column to ISO 8601 where possible")
        # Treat "Unknown" as missing for parsing
        series_for_parse = df["date"].replace("Unknown", pd.NA)
        parsed = pd.to_datetime(series_for_parse, errors="coerce", utc=False)
        df["date"] = parsed.dt.strftime("%Y-%m-%dT%H:%M:%S")
        df["date"] = df["date"].where(df["date"].notna(), "Unknown")

    # Write cleaned CSV
    logging.info("Writing cleaned CSV: %s", output_path)
    df.to_csv(output_path, index=False, encoding="utf-8")

    if preview:
        logging.info("Preview of cleaned data (first 5 rows):\n%s", df.head().to_string(index=False))

    return {
        "input_rows": original_rows,
        "output_rows": len(df),
        "duplicates_removed": duplicates_removed,
        "output_path": str(output_path),
    }


def _parse_args(argv=None):
    p = argparse.ArgumentParser(description="Clean Tick Sightings Excel -> CSV")
    p.add_argument("input", help="Path to Tick Sightings Excel file (e.g. Tick Sightings.xlsx)")
    p.add_argument("-o", "--output", help="Path for cleaned CSV output (default: cleaned_tick_sightings.csv next to input)")
    p.add_argument("-s", "--sheet", default="Sheet1", help="Excel sheet name (default: Sheet1)")
    p.add_argument("--preview", action="store_true", help="Print a preview of the cleaned data (first 5 rows)")
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    try:
        res = clean_data(
            input_path=args.input,
            output_path=args.output,
            sheet_name=args.sheet,
            preview=args.preview,
        )
    except Exception as e:
        logging.error("Processing failed: %s", e)
        sys.exit(1)

    logging.info(
        "Done: input_rows=%d output_rows=%d duplicates_removed=%d output_file=%s",
        res["input_rows"],
        res["output_rows"],
        res["duplicates_removed"],
        res["output_path"],
    )


if __name__ == "__main__":
    main()