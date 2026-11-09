"""Build Excel-ready attrition tables and a department chart."""

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from attrition_package import build_package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "sample_hr_attrition_synthetic.csv",
        help="CSV input file (defaults to the included synthetic sample)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "outputs",
        help="directory for the four CSV reports and chart",
    )
    arguments = parser.parse_args()

    output_files = build_package(arguments.input, arguments.output_dir)
    print("Created attrition data package:")
    for output_file in output_files:
        print(f"- {output_file}")


if __name__ == "__main__":
    main()