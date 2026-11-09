# Attrition Data Package Builder turns fictional employee records into four Excel-ready reports and one chart.
It demonstrates repeatable workforce analysis with small Python tools.
It connects data preparation and workforce insights to HR internship work, without making claims about any employer's workforce.

## Problem

HR teams often need a repeatable way to turn employee records into clear summary tables. This project creates those summaries for practice and presentation; it is not an HR decision tool.

## Data

The included `data/sample_hr_attrition_synthetic.csv` contains 20 made-up employee records, labeled `SYNTHETIC`. No real employee, JPMorganChase, or confidential data is included. The loader expects the core columns used by the public IBM HR Analytics attrition dataset, but this repository does not include or download that dataset.

Only `Attrition`, `Department`, `JobRole`, `OverTime`, and `YearsAtCompany` are retained for analysis. Any other input columns, including `Age`, `Gender`, and `MaritalStatus`, are dropped by the loader before analysis.

## Approach

For each group, the attrition rate is:

`number of employees with Attrition = Yes / number of employees in the group`

This is a proportion from 0 to 1, not a prediction. Each input row is treated as one employee record. The tenure bands are `0-2`, `3-5`, `6-10`, and `11+` years; the first three ranges include both endpoints. Missing required columns cause a clear error rather than a partial report.

The builder creates four CSV tables with employee counts, attrition counts, and attrition rates, plus a bar chart of department rates. CSV files can be opened in Excel. The chart displays rates as percentages.

## Results

These observations are calculated from the included 20-row synthetic sample only. They are examples of how to describe the generated output, not findings about any real workforce:

1. The sample has an overall attrition rate of 8 out of 20 records (0.40).
2. Sales has the highest department rate in this sample: 3 of 6 records (0.50).
3. The sample's 0-2 year tenure band has 6 of 6 records marked as attrition (1.00); the small, deliberately made-up sample cannot support a general conclusion.

## Limitations

- The sample is tiny and synthetic, so rates are illustrative and do not generalize to a real workforce.
- Group rates describe this dataset; they do not establish cause and effect or predict who will leave.
- The analysis intentionally excludes protected-characteristic columns and does not provide employee-level recommendations.
- Results depend on consistent `Yes`/`No` attrition values and valid years-at-company values.

## How to run

Use Python 3.9 or newer. From the repository root, install the dependencies and build the package:

```bash
python -m pip install -r requirements.txt
python build_package.py
```

The command reads only the included synthetic sample by default and creates `outputs/attrition_by_department.csv`, `outputs/attrition_by_job_role.csv`, `outputs/attrition_by_overtime.csv`, `outputs/attrition_by_tenure_band.csv`, and `outputs/attrition_by_department.png`.

Run the automated tests with:

```bash
pytest
```

## Built with AI assistance

AI assistance was used to help draft and check the loader, summary calculations, chart, tests, and documentation. The calculations and assumptions are documented above so they can be reviewed and explained.

Dependencies: pandas reads and groups the CSV data; matplotlib creates the chart; pytest runs the automated tests.