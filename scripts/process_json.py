import json
import pandas as pd
import os
from datetime import datetime

# Ensure output directory exists
output_dir = "./data"
os.makedirs(output_dir, exist_ok=True)  # ✅ Create directory if missing

# Define input and output file paths
input_filename = "./threat_advisories.json"
output_filename = os.path.join(output_dir, "threat_advisories_processes.json")

# 🔹 Step 1: Load JSON Data
try:
    with open(input_filename, "r", encoding="utf-8") as file:
        raw_data = json.load(file)
except FileNotFoundError:
    print(f"❌ Error: {input_filename} not found!")
    exit(1)

# Debug: Check if input data is empty
if not raw_data:
    print("❌ Error: The input JSON file is empty!")
    exit(1)

print(f"✅ Loaded {len(raw_data)} records from {input_filename}")

# 🔹 Step 2: Convert JSON to DataFrame
df = pd.DataFrame(raw_data)

# Ensure column names are trimmed
df.columns = df.columns.str.strip()

# Debug: Print column names
print(f"📊 Columns in dataset: {list(df.columns)}")

# 🔹 Step 3: Add Timestamp
df["timestamp"] = datetime.now().isoformat()

# 🔹 Step 4: Group Data by "Threat Type" and Count
if "Threat Type" in df.columns:
    threat_counts = df["Threat Type"].value_counts().reset_index()
    threat_counts.columns = ["Threat Type", "Count"]
else:
    print("⚠️ Warning: 'Threat Type' column not found! Creating empty DataFrame.")
    threat_counts = pd.DataFrame(columns=["Threat Type", "Count"])

# Debug: Print grouped data
print("🔹 Processed threat counts:")
print(threat_counts)

# 🔹 Step 5: Format Data for Grafana
grafana_data = {
    "columns": [
        {"text": "Threat Type", "type": "string"},
        {"text": "Count", "type": "number"},
        {"text": "Timestamp", "type": "time"}
    ],
    "rows": threat_counts.assign(Timestamp=datetime.now().isoformat()).values.tolist()
}

# Debug: Print final JSON before saving
print("📝 Saving the following data to Grafana JSON format:")
print(json.dumps(grafana_data, indent=2))

# 🔹 Step 6: Save as JSON
with open(output_filename, "w", encoding="utf-8") as file:
    json.dump(grafana_data, file, indent=4)

print(f"✅ Grafana-ready JSON saved: {output_filename}")


# import json
# import pandas as pd
# import os
# from datetime import datetime

# # Ensure output directory exists
# output_dir = "./data"
# os.makedirs(output_dir, exist_ok=True)  # ✅ Create directory if missing

# # Load the raw JSON file
# input_filename = "./threat_advisories.json"
# output_filename = os.path.join(output_dir, "threat_advisories_processes.json")

# try:
#     with open(input_filename, "r", encoding="utf-8") as file:
#         raw_data = json.load(file)
# except FileNotFoundError:
#     print(f"❌ Error: {input_filename} not found!")
#     exit(1)

# # Convert raw data to Pandas DataFrame
# df = pd.DataFrame(raw_data)

# # Ensure columns are trimmed
# df.columns = df.columns.str.strip()

# # Add a timestamp column (if not already present)
# df["timestamp"] = datetime.now().isoformat()

# # Group by "Threat Type" and count occurrences
# if "Threat Type" in df.columns:
#     threat_counts = df["Threat Type"].value_counts().reset_index()
#     threat_counts.columns = ["Threat Type", "Count"]
# else:
#     threat_counts = pd.DataFrame(columns=["Threat Type", "Count"])  # Empty DataFrame as fallback

# # Format DataFrame to match Grafana expected JSON format
# grafana_data = {
#     "columns": [
#         {"text": "Threat Type", "type": "string"},
#         {"text": "Count", "type": "number"},
#         {"text": "Timestamp", "type": "time"}
#     ],
#     "rows": threat_counts.assign(Timestamp=datetime.now().isoformat()).values.tolist()
# }

# # Save as JSON (Grafana format)
# with open(output_filename, "w", encoding="utf-8") as file:
#     json.dump(grafana_data, file, indent=4)

# print(f"✅ Grafana-ready JSON saved: {output_filename}")
