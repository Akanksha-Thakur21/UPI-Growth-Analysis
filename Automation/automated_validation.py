import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent.parent / "Cleaned_UPI_Data.csv"

data = pd.read_csv(file_path)

print(data.head())
print("Dataset Shape:", data.shape)

required_columns = [
    "Month",
    "No. of Banks live on UPI",
    "Volume (In Mn.)",
    "Value (In Cr.)",
    "Financial Year"
]

print("\n--- Column Validation ---")

for column in required_columns:
    if column in data.columns:
        print(column, ": Present")
    else:
        print(column, ": Missing")

print("\n--- Missing Value Check ---")

missing_values = data.isnull().sum()

print(missing_values)

if missing_values.sum() == 0:
    print("No missing values found.")
else:
    print("Missing values detected!")

print("\n--- Duplicate Check ---")

duplicate_rows = data.duplicated().sum()
duplicate_months = data["Month"].duplicated().sum()

print("Duplicate Rows:", duplicate_rows)
print("Duplicate Months:", duplicate_months)

if duplicate_rows == 0 and duplicate_months == 0:
    print("No duplicates found.")
else:
    print("Duplicates detected!")

print("\n--- Data Type Validation ---")

numeric_columns = [
    "No. of Banks live on UPI",
    "Volume (In Mn.)",
    "Value (In Cr.)",
    "Financial Year"
]

for column in numeric_columns:
    if pd.api.types.is_numeric_dtype(data[column]):
        print(column, ": Valid Numeric Type")
    else:
        print(column, ": Invalid Data Type")

print("\n--- Negative Value Check ---")

check_columns = [
    "No. of Banks live on UPI",
    "Volume (In Mn.)",
    "Value (In Cr.)"
]

for column in check_columns:
    negative_values = (data[column] < 0).sum()
    print(column, ":", negative_values, "negative values")

if (data[check_columns] < 0).any().any():
    print("Negative values detected!")
else:
    print("No negative values found.")

print("\n--- Month Date Validation ---")

data["Month"] = pd.to_datetime(data["Month"], errors="coerce")

invalid_dates = data["Month"].isnull().sum()

print("Invalid Dates:", invalid_dates)

if invalid_dates == 0:
    print("All month dates are valid.")
else:
    print("Invalid month dates detected!")

print("\n--- Month Sequence Validation ---")

data = data.sort_values("Month")

expected_months = pd.date_range(
    start="2016-04-01",
    end="2026-03-01",
    freq="MS"
)

actual_months = data["Month"]

missing_months = expected_months.difference(actual_months)
extra_months = actual_months[~actual_months.isin(expected_months)]

print("Expected Months:", len(expected_months))
print("Actual Months:", len(actual_months))
print("Missing Months:", len(missing_months))
print("Extra Months:", len(extra_months))

if len(missing_months) == 0 and len(extra_months) == 0:
    print("Month sequence is complete.")
else:
    print("Month sequence has issues.")

print("\n--- Financial Year Validation ---")

expected_fy = (
    data["Month"].dt.year +
    (data["Month"].dt.month >= 4).astype(int) * 0
)

expected_fy = data["Month"].dt.year.where(
    data["Month"].dt.month < 4,
    data["Month"].dt.year
)

expected_fy = data["Month"].dt.year.where(
    data["Month"].dt.month >= 4,
    data["Month"].dt.year - 1
)

invalid_fy = (data["Financial Year"] != expected_fy).sum()

print("Incorrect Financial Year Records:", invalid_fy)

if invalid_fy == 0:
    print("All financial years are valid.")
else:
    print("Financial year mismatches detected!")

print("\n--- Automated Yearly Analysis ---")

yearly_data = data.groupby("Financial Year").agg({
    "Volume (In Mn.)": "sum",
    "Value (In Cr.)": "sum",
    "No. of Banks live on UPI": "max"
}).reset_index()

yearly_data.rename(columns={
    "Volume (In Mn.)": "Transaction Volume (Mn.)",
    "Value (In Cr.)": "Transaction Value (Cr.)",
    "No. of Banks live on UPI": "Banks Live on UPI"
}, inplace=True)

yearly_data["Average Transaction Value (Rs.)"] = (
    yearly_data["Transaction Value (Cr.)"] * 10 /
    yearly_data["Transaction Volume (Mn.)"]
)

print(yearly_data.head())
print("\nYearly Dataset Shape:", yearly_data.shape)

print("\n--- Yearly Growth Calculation ---")

yearly_data["Volume Growth (%)"] = (
    yearly_data["Transaction Volume (Mn.)"].pct_change() * 100
)

yearly_data["Value Growth (%)"] = (
    yearly_data["Transaction Value (Cr.)"].pct_change() * 100
)

yearly_data["Average Value Growth (%)"] = (
    yearly_data["Average Transaction Value (Rs.)"].pct_change() * 100
)

print(yearly_data)

print("\n--- Automated Insights ---")

highest_volume_year = yearly_data.loc[
    yearly_data["Volume Growth (%)"].idxmax(), "Financial Year"
]

highest_value_year = yearly_data.loc[
    yearly_data["Value Growth (%)"].idxmax(), "Financial Year"
]

latest_year = yearly_data.iloc[-1]

insights = [
    f"Highest volume growth occurred in FY {highest_volume_year}.",

    f"Highest value growth occurred in FY {highest_value_year}.",

    f"UPI transaction volume in the latest financial year was "
    f"{latest_year['Transaction Volume (Mn.)']:,.2f} million.",

    f"UPI transaction value in the latest financial year was "
    f"Rs. {latest_year['Transaction Value (Cr.)']:,.2f} crore.",

    f"There were {latest_year['Banks Live on UPI']} banks live on UPI "
    f"in FY {latest_year['Financial Year']}."
]

for insight in insights:
    print("-", insight)

from pathlib import Path

print("\n--- Saving Insights Report ---")

report_path = Path(__file__).resolve().parent / "Insights_Report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write("UPI TRANSACTION GROWTH - AUTOMATED INSIGHTS\n")
    file.write("=" * 50 + "\n\n")

    for insight in insights:
        file.write("- " + insight + "\n")

print("Insights report saved successfully!")
print("File Location:", report_path)

print("\n--- Saving Validation Report ---")

validation_path = Path(__file__).resolve().parent / "Validation_Report.txt"

with open(validation_path, "w", encoding="utf-8") as file:
    file.write("UPI DATA VALIDATION REPORT\n")
    file.write("=" * 40 + "\n\n")

    file.write(f"Dataset Shape: {data.shape}\n")
    file.write(f"Missing Values: {data.isnull().sum().sum()}\n")
    file.write(f"Duplicate Rows: {data.duplicated().sum()}\n")
    file.write(f"Duplicate Months: {data['Month'].duplicated().sum()}\n")
    file.write(f"Invalid Dates: {data['Month'].isnull().sum()}\n")
    file.write(f"Negative Values: {(data[check_columns] < 0).sum().sum()}\n")

    file.write("\nValidation completed successfully.")

print("Validation report saved successfully!")
print("File Location:", validation_path)


print("\n--- Generating Final Validation Report ---")

checks = {
    "Missing Values": data.isnull().sum().sum() == 0,
    "Duplicate Rows": data.duplicated().sum() == 0,
    "Duplicate Months": data["Month"].duplicated().sum() == 0,
    "Invalid Dates": data["Month"].notnull().all(),
    "Negative Values": not (data[check_columns] < 0).any().any(),
    "Financial Year": invalid_fy == 0,
    "Month Sequence": len(missing_months) == 0 and len(extra_months) == 0
}

validation_path = Path(__file__).resolve().parent / "Validation_Report.txt"

with open(validation_path, "w", encoding="utf-8") as file:
    file.write("UPI DATA VALIDATION REPORT\n")
    file.write("=" * 40 + "\n\n")

    for name, result in checks.items():
        status = "PASS" if result else "FAIL"
        file.write(f"{name}: {status}\n")

    file.write("\nOverall Status: ")
    file.write("PASS" if all(checks.values()) else "FAIL")

print("Validation Report Updated!")
print("Overall Status:", "PASS" if all(checks.values()) else "FAIL")


print("\n--- Saving Yearly Analysis ---")

output_path = Path(__file__).resolve().parent / "Yearly_UPI_Analysis_Automated.csv"

yearly_data.to_csv(output_path, index=False)

print("Yearly analysis saved successfully!")
print("File Location:", output_path)

print("\n--- Comparing Yearly Analysis ---")

original_path = Path(__file__).resolve().parent.parent / "Yearly_UPI_Analysis.csv"

original_data = pd.read_csv(original_path)

try:
    pd.testing.assert_frame_equal(
        yearly_data.reset_index(drop=True),
        original_data.reset_index(drop=True),
        check_dtype=False,
        check_exact=False,
        rtol=1e-5,
        atol=0.01
    )

    print("Comparison Successful!")
    print("Automated analysis matches original analysis.")

except AssertionError as error:
    print("Comparison Failed!")
    print(error)


print("\n--- Automation Summary ---")

total_checks = 7

passed_checks = sum([
    data.isnull().sum().sum() == 0,
    data.duplicated().sum() == 0,
    data["Month"].duplicated().sum() == 0,
    data["Month"].notnull().all(),
    not (data[check_columns] < 0).any().any(),
    invalid_fy == 0,
    len(missing_months) == 0 and len(extra_months) == 0
])

failed_checks = total_checks - passed_checks

print("Total Validation Checks:", total_checks)
print("Passed Checks:", passed_checks)
print("Failed Checks:", failed_checks)
print("Financial Years Analyzed:", len(yearly_data))
print("Monthly Records Analyzed:", len(data))

if failed_checks == 0:
    print("Automation Status: SUCCESS")
else:
    print("Automation Status: COMPLETED WITH ERRORS")


