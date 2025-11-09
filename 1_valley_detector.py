import sys
import pandas as pd
import numpy as np
from scipy.ndimage import minimum_filter1d

refff=sys.argv[1]

def detect_valleys_with_minima(df, valley_threshold=25, valley_width=5):

    valleys_dict = {}
    binary_df = pd.DataFrame(index=df.index, columns=df.columns, dtype=int)

    for idx, row in df.iterrows():
        row_array = row.values.astype(float)
        valley_profile = minimum_filter1d(row_array, size=valley_width)
        binary_mask = valley_profile < valley_threshold

        # Save binary representation
        binary_df.loc[idx] = binary_mask.astype(int)

        # Detect valleys and their minima
        in_valley = False
        start = None
        sample_valleys = []

        for i in range(len(binary_mask)):
            if binary_mask[i] and not in_valley:
                in_valley = True
                start = i
            elif not binary_mask[i] and in_valley:
                in_valley = False
                end = i
                valley_segment = row_array[start:end]
                min_val = np.min(valley_segment)
                min_positions = np.where(valley_segment == min_val)[0]
                first_min_pos = start + min_positions[0]
                sample_valleys.append((start, end, first_min_pos, min_val))

        # If a valley continues to the last position
        if in_valley:
            end = len(binary_mask)
            valley_segment = row_array[start:end]
            min_val = np.min(valley_segment)
            min_positions = np.where(valley_segment == min_val)[0]
            first_min_pos = start + min_positions[0]
            sample_valleys.append((start, end, first_min_pos, min_val))

        valleys_dict[idx] = sample_valleys

    return valleys_dict, binary_df


# Load your input table
df = pd.read_csv(f'./{refff}_v_3mbpan.txt', sep=",", index_col=0)

# Run valley detection
valleys, binary_matrix = detect_valleys_with_minima(df)

# Save binary matrix
#binary_matrix.to_csv("binary_polymorphisms.tsv", sep="\t")

# Save valley info to a readable TSV
with open(f'./{refff}_valley_positions.tsv', "w") as f:
    f.write("Sample\tValleyStart\tValleyEnd\tFirstMinPosition\tMinValue\n")
    for sample, v_list in valleys.items():
        for start, end, min_pos, val in v_list:
            f.write(f"{sample}\t{start}\t{end}\t{min_pos}\t{val:.2f}\n")