import pandas as pd
import yaml

# Load dataset
csv_file = "cardekho_imputated.csv"  # Change this to your actual CSV file name
df = pd.read_csv(csv_file)

# Assuming all columns are numerical (int64) as per your tutor's format
schema = {
    "columns": {col: "int64" for col in df.columns},
    "numerical_columns": list(df.columns)
}

# Save schema to YAML file
yaml_file = "schema.yaml"
with open(yaml_file, "w") as f:
    yaml.dump(schema, f, default_flow_style=False)

print(f"✅ schema.yaml generated successfully from {csv_file}!")
