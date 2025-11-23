# DataReporting.py
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def generate_report(csv_path, output="report.txt"):
    """
    Generates a text summary report including:
    - Total sightings
    - Sightings per region / location
    - Weekly & Monthly Trends
    """

    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # Confirm required fields exist
    if "date" not in df.columns:
        raise ValueError("CSV must include a 'date' column.")
    if "location" not in df.columns:
        raise ValueError("CSV must include a 'location' column.")

    # Convert Date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Build report content
    lines = []
    lines.append("=== Tick Sighting Report ===\n\n")
    lines.append(f"Total sightings: {len(df)}\n")

    # -------------------------
    # Regional Summary
    # -------------------------
    lines.append("\n--- Sightings per Region ---\n")
    region_counts = df["location"].value_counts()
    for region, count in region_counts.items():
        lines.append(f"{region}: {count}\n")

    # -------------------------
    # Monthly trend
    # -------------------------
    df["Month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("Month").size()

    lines.append("\n--- Monthly Trend (Sightings per Month) ---\n")
    for month, count in monthly.items():
        lines.append(f"{month}: {count}\n")

    # -------------------------
    # Weekly trend
    # -------------------------
    df["Week"] = df["date"].dt.to_period("W")
    weekly = df.groupby("Week").size()

    lines.append("\n--- Weekly Trend (Sightings per Week) ---\n")
    for week, count in weekly.items():
        lines.append(f"{week}: {count}\n")

    # Save the report
    output = Path(output)
    output.write_text("".join(lines), encoding="utf-8")

    logging.info(f"Report generated successfully → {output}")
    return output
