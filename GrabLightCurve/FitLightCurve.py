################################################################################
# Fit Light Curve

"""
OVERVIEW:
This program runs the main script for monsoon to get the "cycle", 
"asteroid_id", "reduced_chi2", "peak_power", "period_(hr)", "amplitude", and 
"num_observations" for each asteroid.

IMPORTANT:
For this program to work the researcher needs to put both csv files
cycle1.csv and cycle2.csv in a folder called Observations. Run
DownloadMongoDB.ipynb to get the files. You will have to manually
put these new files in the Observations folder which will be located
in the same folder as this file.
"""

"""
Headers for Cycle1 DF (Northern Hemisphere):
_id, Original_Object_ID, MDJ, Magnitude, Magnitude_Error

Cycle1 Size: 28878 Asteroids

Headers for Cycle2 DF (Southern Hemisphere):
_id, Object_ID, MDJ, Magnitude, Magnitude_Error, Sector

Cycle2 Size: 18712 Asteroids

Overlap Size: 3025 Asteroids
"""

# Created by Group 1

################################################################################
# Imports
from astropy.timeseries import LombScargle
import numpy as np
import pandas as pd
import sys

################################################################################
# Constants

    # None

################################################################################
# Main Program
def main():

    # get args for core number
    cores = int(sys.argv[1])
    core_num = int(sys.argv[2])

    # import data from csv file into a pandas df
    print("importing data...")
    cycle1_df = pd.read_csv("Observations/cycle1.csv", low_memory=False)
    cycle2_df = pd.read_csv("Observations/cycle2.csv", low_memory=False)

    # compute all results
    print("find cycle 1 results...")
    cycle1_results_df = find_cycle_asteroids_light_curve_fit(cycle1_df, "Original_Object_ID", 1, cores, core_num)

    print("find cycle 2 results...")
    cycle2_results_df = find_cycle_asteroids_light_curve_fit(cycle2_df, "Object_ID", 2, cores, core_num)

    # convert dataframes to csv
    print("convert results to csv files...")
    cycle1_results_df.to_csv(f'core{core_num}_cycle1_results.csv', index=False)
    cycle2_results_df.to_csv(f'core{core_num}_cycle2_results.csv', index=False)

################################################################################
# Supporting Functions

def find_asteroid_light_curve(asteroid_info):
        
        asteroid, cycle_num, object_id = asteroid_info
        
        # extract MJD, magnitude, magnitude error
        time_mdj = asteroid["MJD"].values
        magnitude = asteroid["Magnitude"].values
        error = asteroid["Magnitude_Error"].values

        # define frequency range (1 to 24 hours period = 1/24 to 1 cycles/hour)
        # convert MJD to hours relative to first timestamp
        time_hours = (time_mdj - time_mdj.min()) * 24
        frequency = np.linspace(1/(max(time_hours) - min(time_hours)), 1/2, 1000000)
        power = LombScargle(time_hours, magnitude, error).power(frequency)

        # best period is 1 / frequency at peak power
        peak_index = np.argmax(power)
        peak_power = power[peak_index]
        best_frequency = frequency[peak_index]
        best_period = 1 / best_frequency

        # double the period for full rotation
        best_period = best_period * 2

        # compute sine curve fit
        time_fit_hours = np.linspace(0, best_period, 1000)
        ls = LombScargle(time_hours, magnitude, error)
        magnitude_fit_smoothed = ls.model(time_fit_hours, best_frequency)
        magnitude_fit = ls.model(time_hours, best_frequency)

        # get data to scrape
        amplitude = max(magnitude_fit_smoothed) - min(magnitude_fit_smoothed)
        reduced_chi2_statistic = reduced_chi_square(magnitude, magnitude_fit, error)

        return [cycle_num, object_id, reduced_chi2_statistic, 
                peak_power, best_period, amplitude, len(time_mdj)]

def find_cycle_asteroids_light_curve_fit(cycle_df, id_col_name, cycle_num, cores, core_num):

    # initialize output df
    columns = ["cycle", "asteroid_id", "reduced_chi2", "peak_power", 
               "period_(hr)", "amplitude", "num_observations"]
    
    results_df = pd.DataFrame(columns=columns)

    count = 0

    # group each asteroid by their object id
    asteroids = cycle_df.groupby(id_col_name)

    # plot each asteroid
    for object_id, asteroid in asteroids:

        # check specific section
        if count % cores == core_num:

            asteroid_info = (asteroid, cycle_num, object_id)

            result = find_asteroid_light_curve(asteroid_info)

            # add data to the results dataframe
            results_df.loc[len(results_df)] = result

            print(f"asteroid: {count}")

        count += 1

    return results_df

# calculates the chi2 value based on the observed, expected, and error values
def reduced_chi_square(observed, expected, error):

    chi2 = 0

    for observation in range(0, len(observed)):
        chi2 += ((observed[observation] - expected[observation]) ** 2) / error[observation]

    chi2 = chi2 / len(observed - 4)

    return chi2

# defines the sine function to fit on the light curve plot
def sine_function(x, amplitude, frequency, phase, offset):
    
    return amplitude * np.sin(frequency * x + phase) + offset

################################################################################
main()