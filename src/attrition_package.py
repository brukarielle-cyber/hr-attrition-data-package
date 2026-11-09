"""Load synthetic HR records and calculate simple attrition summaries."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


REQUIRED_COLUMNS = [
    "Attrition",
    "Department",
    "JobRole",
    "OverTime",
    "YearsAtCompany",
]
TENURE_BANDS = ["0-2", "3-5", "6-10", "11+"]


def load_data(csv_path):
    """Read a CSV, validate its analysis columns, and discard all other fields."""
    csv_path = Path(csv_path)
    if not csv_path.is_file():
        raise FileNotFoundError(
            f"Input CSV was not found: {csv_path}. "
            "Use the included synthetic sample or provide a valid CSV path."
        )

    data = pd.read_csv(csv_path)
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in data.columns
    ]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Input CSV is missing required columns: {missing}")

    # Keeping only these fields removes protected and unrelated columns up front.
    data = data[REQUIRED_COLUMNS].copy()
    data["YearsAtCompany"] = pd.to_numeric(data["YearsAtCompany"], errors="raise")

    if not data["Attrition"].isin(["Yes", "No"]).all():
        raise ValueError("Attrition values must be 'Yes' or 'No'.")
    if (data["YearsAtCompany"] < 0).any():
        raise ValueError("YearsAtCompany values cannot be negative.")

    return data


def summarize_by(data, group_column):
    """Return group sizes, attrition counts, and attrition proportions."""
    summary = (
        data.groupby(group_column, observed=True)["Attrition"]
        .agg(
            total_employees="size",
            attrition_count=lambda values: values.eq("Yes").sum(),
        )
        .reset_index()
    )
    summary["attrition_rate"] = (
        summary["attrition_count"] / summary["total_employees"]
    )
    return summary


def build_summaries(data):
    """Create the four requested tables from validated employee records."""
    data = data.copy()
    data["TenureBand"] = pd.cut(
        data["YearsAtCompany"],
        bins=[-1, 2, 5, 10, float("inf")],
        labels=TENURE_BANDS,
    )

    return {
        "department": summarize_by(data, "Department"),
        "job_role": summarize_by(data, "JobRole"),
        "overtime": summarize_by(data, "OverTime"),
        "tenure_band": summarize_by(data, "TenureBand"),
    }


def build_package(csv_path, output_dir):
    """Write four CSV reports and a department attrition-rate chart."""
    data = load_data(csv_path)
    summaries = build_summaries(data)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_files = []
    report_names = {
        "department": "attrition_by_department.csv",
        "job_role": "attrition_by_job_role.csv",
        "overtime": "attrition_by_overtime.csv",
        "tenure_band": "attrition_by_tenure_band.csv",
    }
    for summary_name, file_name in report_names.items():
        report_path = output_dir / file_name
        summaries[summary_name].to_csv(report_path, index=False)
        output_files.append(report_path)

    department_summary = summaries["department"]
    chart_path = output_dir / "attrition_by_department.png"
    plt.figure(figsize=(8, 5))
    plt.bar(
        department_summary["Department"],
        department_summary["attrition_rate"],
        color="#287271",
    )
    plt.title("Attrition Rate by Department (Synthetic Sample)")
    plt.xlabel("Department")
    plt.ylabel("Attrition rate")
    plt.ylim(0, 1)
    plt.gca().yaxis.set_major_formatter(
        plt.matplotlib.ticker.PercentFormatter(xmax=1)
    )
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    plt.close()
    output_files.append(chart_path)

    return output_files