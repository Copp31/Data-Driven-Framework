import pandas as pd
import json
from migrant_data_to_midi import MigrantDataToMIDI


# Load the dataset
file_path = '../data/Missing_Migrants_Global_Figures_allData.csv'
df = pd.read_csv(file_path)

# Clean column names (remove quotes and whitespace)
df.columns = df.columns.str.strip().str.replace('"', '')

# Clean and prepare data
df['Number of Dead'] = df['Number of Dead'].fillna(0)
df['Minimum Estimated Number of Missing'] = df['Minimum Estimated Number of Missing'].fillna(0)
df['Total Number of Dead and Missing'] = df['Total Number of Dead and Missing'].fillna(0)
df['Number of Survivors'] = df['Number of Survivors'].fillna(0)
df['Incident Year'] = df['Incident Year'].fillna(0).astype(int)
df['Cause of Death'] = df['Cause of Death'].fillna("Unknown")
df['Migration Route'] = df['Migration Route'].fillna("Unknown")
df['Region of Origin'] = df['Region of Origin'].fillna("Unknown")

# Cross-analysis: total deaths by migration route
deaths_by_route = df.groupby('Migration Route')['Total Number of Dead and Missing'].sum().sort_values(ascending=False).head(10)

# Cross-analysis: cause of death by migration route
death_causes_by_route = df.groupby(['Migration Route', 'Cause of Death'])['Total Number of Dead and Missing'].sum().sort_values(ascending=False).head(15)

# Cross-analysis: origin region by region of incident
origin_by_region = df.groupby(['Region of Incident', 'Region of Origin']).size().sort_values(ascending=False).head(15)

# Years with the most children involved
children_by_year = df.groupby('Incident Year')['Number of Children'].sum().sort_values(ascending=False).head(10)

# Survivor ratio per year
df['Survivor Ratio'] = df['Number of Survivors'] / df['Total Number of Dead and Missing'].replace(0, 1)
avg_ratio_by_year = df.groupby('Incident Year')['Survivor Ratio'].mean().sort_index()

# Write complex text report
report = []

report.append("=== Deep Cross Analysis of the Missing Migrants Project Data ===\n")

report.append("--- Deadliest migration routes ---")
for route, deaths in deaths_by_route.items():
    report.append(f"{route} : {int(deaths)} dead/missing")

report.append("\n--- Leading causes of death by migration route ---")
for (route, cause), deaths in death_causes_by_route.items():
    report.append(f"{route} — {cause} : {int(deaths)} dead/missing")

report.append("\n--- Migrants' origin by region of incident ---")
for (region, origin), count in origin_by_region.items():
    report.append(f"Incident in {region} — Origin: {origin} : {count} cases")

report.append("\n--- Years with the most children involved ---")
for year, children in children_by_year.items():
    report.append(f"{int(year)} : {int(children)} children involved")

report.append("\n--- Average survivor ratio per year ---")
for year, ratio in avg_ratio_by_year.items():
    report.append(f"{int(year)} : avg ratio = {ratio:.2f}")

# Save the text report
report_path = "../data/analyse_croisee_missing_migrants.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

# Export the same analysis as structured JSON
json_data = {
    "deaths_by_route": deaths_by_route.astype(int).to_dict(),
    "death_causes_by_route": {
        f"{route} — {cause}": int(value)
        for (route, cause), value in death_causes_by_route.items()
    },
    "origin_by_region": {
        f"{region} — {origin}": int(count)
        for (region, origin), count in origin_by_region.items()
    },
    "children_by_year": children_by_year.astype(int).to_dict(),
    "avg_survivor_ratio_by_year": {str(year): round(ratio, 2) for year, ratio in avg_ratio_by_year.items()}
}

json_path = "../data/analyse_croisee_missing_migrants.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

json_path = "../data/analyse_croisee_missing_migrants.json"
output_midi = "../data/children_by_year.mid"

converter = MigrantDataToMIDI(json_path)
converter.create_midi_from_field("children_by_year", output_midi)