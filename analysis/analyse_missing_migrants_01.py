import pandas as pd
import json
from migrant_data_to_midi import MigrantDataToMIDI

# Load the dataset
file_path = '../data/Missing_Migrants_Global_Figures_allData.csv'
df = pd.read_csv(file_path)

# Clean column names (remove extra quotes and whitespace)
df.columns = df.columns.str.strip().str.replace('"', '')

# Fill missing values for numeric analysis
df['Number of Dead'] = df['Number of Dead'].fillna(0)
df['Minimum Estimated Number of Missing'] = df['Minimum Estimated Number of Missing'].fillna(0)
df['Total Number of Dead and Missing'] = df['Total Number of Dead and Missing'].fillna(0)
df['Number of Survivors'] = df['Number of Survivors'].fillna(0)
df['Number of Females'] = df['Number of Females'].fillna(0)
df['Number of Males'] = df['Number of Males'].fillna(0)
df['Number of Children'] = df['Number of Children'].fillna(0)

# Main statistics
total_dead = df['Number of Dead'].sum()
total_missing = df['Minimum Estimated Number of Missing'].sum()
total_dead_and_missing = df['Total Number of Dead and Missing'].sum()
total_survivors = df['Number of Survivors'].sum()
total_females = df['Number of Females'].sum()
total_males = df['Number of Males'].sum()
total_children = df['Number of Children'].sum()

# Top regions where incidents occurred
top_regions = df['Region of Incident'].value_counts().head(5)

# Most frequent causes of death
top_causes = df['Cause of Death'].value_counts().head(5)

# Most common countries of origin
top_origins = df['Country of Origin'].value_counts().head(5)

# Yearly total deaths and missing
deaths_by_year = df.groupby('Incident Year')['Total Number of Dead and Missing'].sum()

# Generate plain-text report
report = []

report.append("=== Analysis of the Missing Migrants Project Data ===\n")

report.append(f"Total confirmed deaths: {int(total_dead):,}")
report.append(f"Estimated number of missing persons: {int(total_missing):,}")
report.append(f"Total number of dead and missing: {int(total_dead_and_missing):,}")
report.append(f"Total number of survivors: {int(total_survivors):,}\n")

report.append("--- Demographic distribution ---")
report.append(f"Total number of females: {int(total_females):,}")
report.append(f"Total number of males: {int(total_males):,}")
report.append(f"Total number of children: {int(total_children):,}\n")

report.append("--- Regions with the most incidents ---")
for region, count in top_regions.items():
    report.append(f"{region}: {count} incidents")

report.append("\n--- Most common causes of death ---")
for cause, count in top_causes.items():
    report.append(f"{cause}: {count} cases")

report.append("\n--- Most frequently recorded countries of origin ---")
for country, count in top_origins.items():
    report.append(f"{country}: {count} cases")

report.append("\n--- Yearly deaths and missing ---")
for year, value in deaths_by_year.items():
    report.append(f"{int(year)}: {int(value)} dead/missing")

# Save as a .txt report
report_path = "../data/analyse_missing_migrants.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

# Save as a .json structured file
json_data = {
    "totals": {
        "total_dead": int(total_dead),
        "total_missing": int(total_missing),
        "total_dead_and_missing": int(total_dead_and_missing),
        "total_survivors": int(total_survivors),
        "total_females": int(total_females),
        "total_males": int(total_males),
        "total_children": int(total_children)
    },
    "top_regions": top_regions.to_dict(),
    "top_causes": top_causes.to_dict(),
    "top_origins": top_origins.to_dict(),
    "deaths_by_year": deaths_by_year.astype(int).to_dict()
}

json_path = "../data/analyse_missing_migrants.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)
