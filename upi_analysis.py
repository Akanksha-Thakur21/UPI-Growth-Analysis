import pandas as pd
import matplotlib.pyplot as plt
import openpyxl 
print("Libraries imported successfully.")
import os
files = os.listdir("Raw_Data")
print("\nExcel files available in the Raw_Data folder:")
for file in files:
    print(file)
print("\nTotal Files:", len(files))
data = pd.read_excel("Raw_Data/" + files[0])
print(data)
# Check dataset shape
print("\nDataset shape:")
print(data.shape)

# check column names
print("\nColumn names:")
print(data.columns)

#Check data types
print("\nData types:")
print(data.dtypes)

#check for missing values
print("\nMissing values:")
print(data.isnull().sum())

# check for duplicate records
print("\nDuplicate records:")
print(data.duplicated().sum())

# now for all files together
all_data = []
for file in files:
    data = pd.read_excel("Raw_Data/" + file)
    all_data.append(data)
print("\nTotal Excel files read",len(all_data))

#Combine all datasets
combined_data = pd.concat(all_data,ignore_index=True)
print("\nCOmbined dataset:")
print(combined_data)

# Check combined dataset shape
print("\nCombined Dataset Shape:")
print(combined_data.shape)

# check for missing values in combined dataset
print("\nMissing values:")
print(combined_data.isnull().sum())

# check for duplicate records in combined dataset
print("\nDuplicate records:")
print(combined_data.duplicated().sum())

#check duplicate months 
print("\nDuplicate months:")
print(combined_data["Month"].duplicated().sum())

#check first 10 months
print("\nFirst 10 rows:")
print(combined_data["Month"].head(10))

# Check last 10 months
print("\nLast 10 rows:")
print(combined_data["Month"].tail(10))

combined_data["Month"] = pd.to_datetime(
    combined_data["Month"],format="%B-%Y"
)

#sort data from oldest to latest
combined_data = combined_data.sort_values("Month")

# Reset index
combined_data = combined_data.reset_index(drop=True)

print("\nChronologically Sorted data:")
print(combined_data[["Month"]])

print("\nFinal Dataset Shape:")
print(combined_data.shape)

# Display first 10 records
print("\nFirst 10 Records:")
print(combined_data.head(10))

# Display last 10 records
print("\nLast 10 Records:")
print(combined_data.tail(10))

print("\nVolume Sample Values:")
print(combined_data["Volume (In Mn.)"].head(10))

print("\nValue Sample Values:")
print(combined_data["Value (In Cr.)"].head(10))

# Remove commas and extra spaces, then convert to numeric

combined_data["Volume (In Mn.)"] = pd.to_numeric(
    combined_data["Volume (In Mn.)"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

combined_data["Value (In Cr.)"] = pd.to_numeric(
    combined_data["Value (In Cr.)"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

print("\nUpdated Column Data Types:")
print(combined_data.dtypes)

#Statistical summary
print("\nStatistical Summary:")
print(combined_data.describe())

# Save cleaned dataset as CSV

combined_data.to_csv("Cleaned_UPI_Data.csv", index=False)

print("\nCleaned dataset saved successfully!")

combined_data["Financial Year"] = combined_data["Month"].dt.year
combined_data.loc[combined_data["Month"].dt.month < 4,"Financial Year"] -= 1
print(combined_data[["Month","Financial Year"]].head(15))

# Year-wise UPI Transaction Volume
yearly_volume = combined_data.groupby("Financial Year")["Volume (In Mn.)"].sum()

print("\nYear-wise Transaction Volume:")
print(yearly_volume)

# Year-wise UPI Transaction Value
yearly_value = combined_data.groupby("Financial Year")["Value (In Cr.)"].sum()
print("\nYear-wise Transaction Value:")
print(yearly_value)

# Volume = How many transactions happened 
# Value = How much money was transfered through those transactions

# Year-wise Bank Participation

yearly_banks = combined_data.groupby("Financial Year")["No. of Banks live on UPI"].last()

print("\nYear-wise Bank Participation:")
print(yearly_banks)

# Average Transaction Value for Each Financial Year

average_transaction_value = (yearly_value / yearly_volume) * 10

print("\nAverage Transaction Value (₹):")
print(average_transaction_value.round(2))

# Year-wise Transaction Volume Growth
volume_growth = yearly_volume.pct_change() * 100

print("\nYear-wise Volume Growth (%):")
print(volume_growth.round(2))

# Year-wise Transaction Value Growth
value_growth = yearly_value.pct_change() * 100
print("\nYear-wise Value Growth (%):")
print(value_growth.round(2))

# Average Transaction Value Growth

average_value_growth = average_transaction_value.pct_change() * 100

print("\nAverage Transaction Value Growth (%):")
print(average_value_growth.round(2))

# Step 12: Combine Yearly Analysis
yearly_analysis = pd.DataFrame({
    "Transaction Volume (Mn.)": yearly_volume,
    "Transaction Value (Cr.)": yearly_value,
    "Banks Live on UPI": yearly_banks,
    "Average Transaction Value (Rs.)": average_transaction_value,
    "Volume Growth (%)": volume_growth,
    "Value Growth (%)": value_growth,
    "Average Value Growth (%)": average_value_growth
})

print("\nYearly UPI Analysis:")
print(yearly_analysis.round(2))
#display all columns in the output
pd.set_option("display.max_columns", None)
print(yearly_analysis.round(2))
# Save Yearly Analysis

yearly_analysis.to_csv("Yearly_UPI_Analysis.csv")

print("Yearly analysis saved successfully!")

# Graph 1: Year-wise UPI Transaction Volume

plt.figure(figsize=(11, 6), facecolor="#F4F7FB")

plt.plot(
    yearly_volume.index,
    yearly_volume.values,
    color="#243B64",
    marker="o",
    linewidth=3,
    markersize=7
)

plt.title(
    "Year-wise UPI Transaction Volume",
    fontsize=16,
    fontweight="bold",
    color="#263238"
)

plt.xlabel("Financial Year", fontsize=12)
plt.ylabel("Transaction Volume (Millions)", fontsize=12)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4,
    color="#DCE3EC"
)

plt.xticks(yearly_volume.index)

plt.tight_layout()
plt.savefig("Graphs/Graph1_Transaction_Volume.png", dpi=300, bbox_inches="tight")

plt.show()
# Graph 2: Year-wise UPI Transaction Value

plt.figure(figsize=(11, 6), facecolor="#F4F7FB")

plt.plot(
    yearly_value.index,
    yearly_value.values,
    color="#00A6A6",
    marker="o",
    linewidth=3,
    markersize=7
)

plt.title(
    "Year-wise UPI Transaction Value",
    fontsize=16,
    fontweight="bold",
    color="#263238"
)

plt.xlabel("Financial Year", fontsize=12)
plt.ylabel("Transaction Value (Crores)", fontsize=12)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4,
    color="#DCE3EC"
)

plt.xticks(yearly_value.index)

plt.tight_layout()
plt.savefig(
    "Graphs/Graph2_Transaction_Value.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# Graph 3: Year-wise Bank Participation

plt.figure(figsize=(11, 6), facecolor="#F4F7FB")

plt.plot(
    yearly_banks.index,
    yearly_banks.values,
    color="#F4B942",
    marker="o",
    linewidth=3,
    markersize=7
)

plt.title(
    "Year-wise Banks Live on UPI",
    fontsize=16,
    fontweight="bold",
    color="#263238"
)

plt.xlabel("Financial Year", fontsize=12)
plt.ylabel("Number of Banks", fontsize=12)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4,
    color="#DCE3EC"
)

plt.xticks(yearly_banks.index)

plt.tight_layout()
plt.savefig(
    "Graphs/Graph3_Banks_Live.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# Graph 4: Average Transaction Value

plt.figure(figsize=(11, 6), facecolor="#F4F7FB")

plt.plot(
    average_transaction_value.index,
    average_transaction_value.values,
    color="#243B64",
    marker="o",
    markerfacecolor="#F4B942",
    linewidth=3,
    markersize=7
)

plt.title(
    "Year-wise Average UPI Transaction Value",
    fontsize=16,
    fontweight="bold",
    color="#263238"
)

plt.xlabel("Financial Year", fontsize=12)
plt.ylabel("Average Transaction Value (₹)", fontsize=12)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4,
    color="#DCE3EC"
)

plt.xticks(average_transaction_value.index)

plt.tight_layout()
plt.savefig(
    "Graphs/Graph3_Banks_Live.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# Graph 5: Volume Growth vs Value Growth

plt.figure(figsize=(11, 6), facecolor="#F4F7FB")

plt.plot(
    volume_growth.index,
    volume_growth.values,
    color="#243B64",
    marker="o",
    linewidth=3,
    markersize=7,
    label="Volume Growth (%)"
)

plt.plot(
    value_growth.index,
    value_growth.values,
    color="#00A6A6",
    marker="o",
    linewidth=3,
    markersize=7,
    label="Value Growth (%)"
)

plt.title(
    "UPI Volume Growth vs Value Growth",
    fontsize=16,
    fontweight="bold",
    color="#263238"
)

plt.xlabel("Financial Year", fontsize=12)
plt.ylabel("Growth Rate (%)", fontsize=12)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4,
    color="#DCE3EC"
)

plt.xticks(volume_growth.index)

plt.legend()

plt.tight_layout()
plt.savefig(
    "Graphs/Graph5_Volume_vs_Value_Growth.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# Graph 6: Recent UPI Growth Comparison

plt.figure(figsize=(11, 6), facecolor="#F4F7FB")

plt.plot(
    volume_growth.loc[2018:].index,
    volume_growth.loc[2018:].values,
    color="#243B64",
    marker="o",
    linewidth=3,
    markersize=7,
    label="Volume Growth (%)"
)

plt.plot(
    value_growth.loc[2018:].index,
    value_growth.loc[2018:].values,
    color="#00A6A6",
    marker="o",
    linewidth=3,
    markersize=7,
    label="Value Growth (%)"
)

plt.title(
    "Recent UPI Volume Growth vs Value Growth",
    fontsize=16,
    fontweight="bold",
    color="#263238"
)

plt.xlabel("Financial Year", fontsize=12)
plt.ylabel("Growth Rate (%)", fontsize=12)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4,
    color="#DCE3EC"
)

plt.xticks(volume_growth.loc[2018:].index)

plt.legend()
plt.tight_layout()
plt.savefig(
    "Graphs/Graph6_Recent_Growth_Comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# Graph 7: Monthly UPI Transaction Volume

plt.figure(figsize=(13, 6), facecolor="#F4F7FB")

plt.plot(
    combined_data["Month"],
    combined_data["Volume (In Mn.)"],
    color="#243B64",
    linewidth=2
)

plt.title(
    "Monthly UPI Transaction Volume Trend (2016–2026)",
    fontsize=16,
    fontweight="bold",
    color="#263238"
)

plt.xlabel("Year", fontsize=12)
plt.ylabel("Transaction Volume (Millions)", fontsize=12)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4,
    color="#DCE3EC"
)

plt.tight_layout()
plt.savefig(
    "Graphs/Graph7_Monthly_Transaction_Volume.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
# Graph 8: Monthly UPI Transaction Value

plt.figure(figsize=(13, 6), facecolor="#F4F7FB")

plt.plot(
    combined_data["Month"],
    combined_data["Value (In Cr.)"],
    color="#00A6A6",
    linewidth=2
)

plt.title(
    "Monthly UPI Transaction Value Trend (2016–2026)",
    fontsize=16,
    fontweight="bold",
    color="#263238"
)

plt.xlabel("Year", fontsize=12)
plt.ylabel("Transaction Value (Crores)", fontsize=12)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4,
    color="#DCE3EC"
)

plt.tight_layout()
plt.savefig(
    "Graphs/Graph8_Monthly_Transaction_Value.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Create folder for saving graphs

os.makedirs("Graphs", exist_ok=True)

print("Graphs folder created successfully!")
print("Dataset Shape:", combined_data.shape)
print("\nMissing Values:")
print(combined_data.isnull().sum())
print("\nDuplicate Records:", combined_data.duplicated().sum())
print("\nColumn Data Types:")
print(combined_data.dtypes)
# Save Final Cleaned Dataset

combined_data.to_csv("Cleaned_UPI_Data.csv", index=False)

print("Final cleaned dataset saved successfully!")