import json
import pandas as pd
from datetime import datetime

# Load the raw JSON file
with open("./threat_advisories.json", "r", encoding="utf-8") as file:
    raw_data = json.load(file)

# Convert raw data to Pandas DataFrame
df = pd.DataFrame(raw_data)

# Ensure columns are trimmed
df.columns = df.columns.str.strip()

# Add a timestamp column (if not already present)
df["timestamp"] = datetime.now().isoformat()

# Group by "Threat Type" and count occurrences
if "Threat Type" in df.columns:
    threat_counts = df["Threat Type"].value_counts().reset_index()
    threat_counts.columns = ["Threat Type", "Count"]
else:
    threat_counts = pd.DataFrame(columns=["Threat Type", "Count"])  # Empty DataFrame as fallback

# Format DataFrame to match Grafana expected JSON format
grafana_data = {
    "columns": [
        {"text": "Threat Type", "type": "string"},
        {"text": "Count", "type": "number"},
        {"text": "Timestamp", "type": "time"}
    ],
    "rows": threat_counts.assign(Timestamp=datetime.now().isoformat()).values.tolist()
}

# Save as JSON (Grafana format)
output_filename = "./data/threat_advisories_processes.json"
with open(output_filename, "w", encoding="utf-8") as file:
    json.dump(grafana_data, file, indent=4)

print(f"✅ Grafana-ready JSON saved: {output_filename}")
