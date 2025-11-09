import sys
import pandas as pd

refff = sys.argv[1]

# Load filtered valley data (must contain 'group_id' and 'Sample')
df = pd.read_csv(f'./{refff}_tolfiltered_valley_positions.tsv', sep="\t")

# Load list of all sample names
with open("sample_names.txt") as f:
    all_samples = [line.strip() for line in f]

# Ensure necessary columns exist
required_cols = {"group_id", "Sample"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Error: Missing columns in input file: {', '.join(missing)}")


# Group by (group_id, Sample), count occurrences
presence_df = (
    df.groupby(["group_id", "Sample"])
    .size()
    .unstack(fill_value=0)     # Convert to wide format: group_id × Sample
    .clip(upper=1)             # Convert counts >1 to 1 (presence)
    .reindex(columns=all_samples, fill_value=0)  # Ensure all samples appear as columns
)

# Compute total presence per sample
presence_df.loc["__TOTAL__"] = presence_df.sum(axis=0)

# Sort columns (samples) by total presence
presence_df = presence_df[presence_df.loc["__TOTAL__"].sort_values().index]

# Save to file
output_path = f'./{refff}_tolpresence_matrix.tsv'
presence_df.to_csv(output_path, sep="\t")