# main.py

import sys
from DataHandling import clean_data
from SearchAndFilter import main as search_main
from DataReporting import generate_report


def run_default():
    """Default behavior: clean the Excel spreadsheet."""
    input_file = "Tick Sightings.xlsx"
    output_file = "cleaned_tick_sightings.csv"

    res = clean_data(
        input_path=input_file,
        output_path=output_file,
        preview=True
    )

    print(
        f"Done: input_rows={res['input_rows']} "
        f"output_rows={res['output_rows']} "
        f"duplicates_removed={res['duplicates_removed']} "
        f"output_file={res['output_path']}"
    )


def run_clean(argv):
    """Explicit clean command."""
    input_file = "Tick Sightings.xlsx"
    output_file = "cleaned_tick_sightings.csv"

    res = clean_data(
        input_path=input_file,
        output_path=output_file,
        preview=True
    )

    print(
        f"Done: input_rows={res['input_rows']} "
        f"output_rows={res['output_rows']} "
        f"duplicates_removed={res['duplicates_removed']} "
        f"output_file={res['output_path']}"
    )


def run_search(argv):
    """
    Forward all search command-line arguments
    to SearchAndFilter.main().
    Example:
        python main.py search --start 2024-01-01 --location London
    """
    return search_main(argv)


def run_report(argv=None):
    """
    Generate a report.

    Usage:
      python main.py report
      python main.py report filtered.csv
    """

    # Default cleaned dataset
    csv_path = "cleaned_tick_sightings.csv"

    # If user provides a file, use that instead
    if argv and len(argv) >= 1:
        csv_path = argv[0]

    output_file = "report.txt"

    try:
        result = generate_report(csv_path, output=output_file)
        print(f"Report successfully created: {result}")
    except Exception as e:
        print(f"Error generating report: {e}")


def _print_usage():
    print("""
Usage: python main.py [command] [options]

Commands:
  clean               Clean the Excel dataset
  search <options>    Search and filter the cleaned data
  report [file]       Generate a report (default: cleaned_tick_sightings.csv)
  help                Show this help message

Examples:
  python main.py clean
  python main.py search --location London --start 2024-01-01
  python main.py report
  python main.py report filtered.csv
""")
    return


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        # no command = default clean
        return run_default()

    command = argv[0]
    args = argv[1:]

    if command == "clean":
        return run_clean(args)

    if command == "search":
        return run_search(args)

    if command == "report":
        return run_report(args)

    if command in ("-h", "--help", "help"):
        return _print_usage()

    print(f"Unknown command: {command}")
    return _print_usage()


if __name__ == "__main__":
    main()

