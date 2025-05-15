################################################################################
# Intersect Data

"""
Overview: This program takes in cycle1 data and cycle2 data and if asteroid 
in both files it will make a new row combining the data into one file.

Expecting CSV files with the following headers:
cycle,asteroid_id,reduced_chi2,peak_power,period_(hr),amplitude,num_observations

Will output the following CSV file with the headers:
asteroid_id, reduced_chi2_1 ,reduced_chi2_2, peak_power_1, peak_power_2,
period_(hr)_1, period_(hr)_2 ,amplitude_1, amplitude_2, num_observations_1, 
num_observations_2
"""

# Created by Group 1
################################################################################
# Imports
import pandas as pd
import os
import sys

################################################################################
# Constants

################################################################################
# Main Program
def main():

    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <cycle1.csv> <cycle2.csv> <output.csv>")
        sys.exit(1)

    # get input files via command line
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]

    # check if input files exist
    for fn in (file1, file2):
        if not os.path.isfile(fn):
            print(f"Error: {fn} not found in {os.getcwd()}")
            sys.exit(1)

    # Load data
    cycle1_df = pd.read_csv(file1)
    cycle2_df = pd.read_csv(file2)

    # Rename columns to identify origin
    suffixes = ['_1', '_2']
    cycle1_df = cycle1_df.rename(columns={
        'reduced_chi2': 'reduced_chi2_1',
        'peak_power': 'peak_power_1',
        'period_(hr)': 'period_(hr)_1',
        'amplitude': 'amplitude_1',
        'num_observations': 'num_observations_1'
    })

    cycle2_df = cycle2_df.rename(columns={
        'reduced_chi2': 'reduced_chi2_2',
        'peak_power': 'peak_power_2',
        'period_(hr)': 'period_(hr)_2',
        'amplitude': 'amplitude_2',
        'num_observations': 'num_observations_2'
    })

    # Drop unnecessary 'cycle' column if present
    if 'cycle' in cycle1_df.columns:
        cycle1_df = cycle1_df.drop(columns=['cycle'])
    if 'cycle' in cycle2_df.columns:
        cycle2_df = cycle2_df.drop(columns=['cycle'])

    # Merge on asteroid_id (inner join to keep only common ones)
    merged_df = pd.merge(cycle1_df, cycle2_df, on='asteroid_id', how='inner')

    # Reorder columns
    merged_df = merged_df[[
        'asteroid_id',
        'reduced_chi2_1', 'reduced_chi2_2',
        'peak_power_1', 'peak_power_2',
        'period_(hr)_1', 'period_(hr)_2',
        'amplitude_1', 'amplitude_2',
        'num_observations_1', 'num_observations_2'
    ]]

    # Save to CSV
    merged_df.to_csv(output_file, index=False)
    print(f"Saved merged data to {output_file} with {len(merged_df)} intersecting asteroids.")


################################################################################
if __name__ == "__main__":
    main()