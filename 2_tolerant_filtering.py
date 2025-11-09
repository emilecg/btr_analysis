import sys
import pandas as pd
import numpy as np

refff = sys.argv[1]

# Load the table
df = pd.read_csv(f'./{refff}_valley_positions.tsv', sep="\t")

# Get the maximum 'ValleyEnd' value
max_valley_end = df['ValleyEnd'].max()

# Apply first two filters
filtered = df[(df['ValleyStart'] != 0) & (df['ValleyEnd'] != max_valley_end)]

# Sort by ValleyStart for faster comparisons
filtered = filtered.sort_values(by=['ValleyStart', 'ValleyEnd']).reset_index(drop=True)

# Create a column marking group IDs based on proximity (±5)
group_id = np.full(len(filtered), -1)
current_group = 0

for i in range(len(filtered)):
    if group_id[i] != -1:
        continue  # already assigned to a group
    # Find all rows within ±5 of both coordinates
    start_val = filtered.loc[i, 'ValleyStart']
    end_val = filtered.loc[i, 'ValleyEnd']
    mask = (
        (np.abs(filtered['ValleyStart'] - start_val) <= 5) &
        (np.abs(filtered['ValleyEnd'] - end_val) <= 5)
    )
    group_id[mask] = current_group
    current_group += 1

filtered['group_id'] = group_id

# Count how many times each approximate pair occurs
group_counts = filtered.groupby('group_id').size().reset_index(name='count')

# Merge and keep only groups with count > 2
filtered = filtered.merge(group_counts, on='group_id')
filtered = filtered[filtered['count'] > 2]

# Drop helper columns
filtered = filtered.drop(columns=['count'])

# Save the result
filtered.to_csv(f'./{refff}_tolfiltered_valley_positions.tsv', sep="\t", index=False)