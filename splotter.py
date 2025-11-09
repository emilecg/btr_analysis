import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster.hierarchy import linkage, leaves_list

def clean_and_load_csv(file_path):
    # Read file and determine max number of columns
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]  # Remove empty rows
        max_cols = max(len(row) for row in rows)  # Find max columns in any row

    # Filter rows that have less than max_cols
    filtered_rows = [row for row in rows if len(row) == max_cols]

    # Convert filtered data into a Pandas DataFrame
    df = pd.DataFrame(filtered_rows)

    # First column is the sample names, convert the rest to numeric
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric)

    return df

def process_csv(file_path):
    df = clean_and_load_csv(file_path)

    # Compute row sums
    df[df.shape[1]] = df.iloc[:, 1:].sum(axis=1)
    # Sort by sum in descending order
    df.sort_values(by=df.columns[-1], ascending=False, inplace=True)
    #print(df)

    # Keep only rows where sum >= half of the maximum sum
    max_sum = df[df.columns[-1]].max()
    df = df[df[df.columns[-1]] >= max_sum / 4]

    # Drop sum column before plotting
    df.drop(columns=[df.columns[-1]], inplace=True)

    # Generate the heatmap plot
    plot_data(df)

def plot_data(df):
    sample_names = df.iloc[:, 0].values  # Extract sample names
    matrix_data = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce").fillna(0).values  # Convert to numeric and fill NaN

    # Set up colormap (inverted viridis: blue for high values, yellow for low values)
    cmap = plt.get_cmap("viridis_r")  # '_r' at the end inverts the colormap

    # Create figure
    fig, ax = plt.subplots(figsize=(100, 200))
    ax.imshow(matrix_data.astype(float), aspect="auto", cmap=cmap, interpolation="nearest")  # Ensure float conversion

    # Add sample names on the left
    ax.set_yticks(range(len(sample_names)))
    ax.set_yticklabels(sample_names, fontsize=8)

    # Hide x-axis labels
    ax.set_xticks([])

    plt.savefig(f'plot.jpg', dpi=100, bbox_inches='tight')



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python splotter.py <input.csv>")
    else:
        process_csv(sys.argv[1])
