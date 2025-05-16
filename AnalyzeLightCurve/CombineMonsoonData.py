################################################################################
# Combine Monsoon Data

"""
OVERVIEW:
Since there were many different scripts running in monsoon this program takes
all of the separated output and combines it into one csv file for cycle1,
cycle2, and the combination of cycle1 and cycle2

IMPORTANT:
In order for this program to work the researcher needs to have a folder called
MonsoonDataReturn in the same folder as this file. It is also important to note
how many different cores (scripts) were used to get all of the data.
"""

# Created by Group 1
################################################################################
# Imports
import sys
import os
import pandas as pd

################################################################################
# Constants

################################################################################
# Main Program
def main():

    # get how many cores were used from cmd line
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <num_cores>")
        sys.exit(1)

    n_cores = int(sys.argv[1])
    data_dir = os.path.join(os.path.dirname(__file__), "MonsoonDataReturn")

    # initialize results
    dfs_cycle1 = []
    dfs_cycle2 = []

    # iterate through each core's files
    for i in range(n_cores):

        # access the file
        prefix = f"core{i}_"
        fn_cycle1 = os.path.join(data_dir, prefix + "cycle1_results.csv")
        fn_cycle2 = os.path.join(data_dir, prefix + "cycle2_results.csv")

        # Read them—if any are missing, warn and skip
        try:
            dfs_cycle1.append(pd.read_csv(fn_cycle1))
        except FileNotFoundError:
            print(f"Warning: {fn_cycle1} not found, skipping.")
        try:
            dfs_cycle2.append(pd.read_csv(fn_cycle2))
        except FileNotFoundError:
            print(f"Warning: {fn_cycle2} not found, skipping.")

    # concatenate and write out
    if dfs_cycle1:
        pd.concat(dfs_cycle1, ignore_index=True).to_csv("cycle1_results.csv", 
                                                                    index=False)
        print("Written cycle1_results.csv")
    else:
        print("No cycle1 data to write.")

    if dfs_cycle2:
        pd.concat(dfs_cycle2, ignore_index=True).to_csv("cycle2_results.csv", 
                                                                    index=False)
        print("Written cycle2_results.csv")
    else:
        print("No cycle2 data to write.")

################################################################################
if __name__ == "__main__":
    main()