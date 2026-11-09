import pandas as pd
import pytest

from src.attrition_package import build_summaries, load_data


def test_loader_rejects_file_with_missing_columns(tmp_path):
    csv_path = tmp_path / "incomplete.csv"
    pd.DataFrame({"Attrition": ["Yes"], "Department": ["Sales"]}).to_csv(
        csv_path, index=False
    )

    with pytest.raises(ValueError, match="missing required columns"):
        load_data(csv_path)


def test_attrition_rates_are_between_zero_and_one():
    data = load_data("data/sample_hr_attrition_synthetic.csv")
    summaries = build_summaries(data)

    for summary in summaries.values():
        assert summary["attrition_rate"].between(0, 1).all()