################################################################################
# Get Cycle Intersection

"""
OVERVIEW:
Gets the asteroid id that appears in both cycle1 and cycle2 and makes a new csv
file tracking those

IMPORTANT:
In order for this program to work the researcher needs to have
cycle1_results.csv and cycle2 results.csv in the same folder as this program
"""

# Created by Group 1
################################################################################
# Imports
import numpy as np
import pandas as pd
import os
import sys

################################################################################
# Constants

    # None

################################################################################
# Main Program
def main():

    # ensure input files exist
    fn1 = "cycle1_results.csv"
    fn2 = "cycle2_results.csv"
    for fn in (fn1, fn2):
        if not os.path.isfile(fn):
            print(f"Error: {fn} not found in {os.getcwd()}")
            sys.exit(1)

    # load the csv file into a dataframe
    cycle1_df = pd.read_csv(fn1, low_memory=False)
    cycle2_df = pd.read_csv(fn2, low_memory=False)

    # we only need asteroid_id, period_(hr), amplitude
    cycle1_df = cycle1_df[["asteroid_id", "period_(hr)", "amplitude"]]
    cycle2_df = cycle2_df[["asteroid_id", "period_(hr)", "amplitude"]]

    # rename columns to id the cycle #
    cycle1_df = cycle1_df.rename(columns={
        "period_(hr)": "period_(hr)_1",
        "amplitude":     "amplitude_1"
    })

    cycle2_df = cycle2_df.rename(columns={
        "period_(hr)": "period_(hr)_2",
        "amplitude":     "amplitude_2"
    })

    # inner‐join on asteroid_id to keep only those present in both
    both = pd.merge(cycle1_df, cycle2_df, on = "asteroid_id", how = "inner")
    both.to_csv("cycle_both_results.csv", index=False)
    print(f"Wrote {len(both)} rows to cycle_both_results.csv")

################################################################################
if __name__ == "__main__":
    main()