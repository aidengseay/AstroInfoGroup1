################################################################################
# Fit Light Curve
# Created by Group 1
################################################################################
# Imports
from astropy.timeseries import LombScargle
import numpy as np
import pandas as pd

################################################################################
# Constants

    # None

################################################################################
# Main Program
def main():

    # import data from csv file into a pandas df
    print("importing data...")
    cycle1_df = pd.read_csv("Observations/cycle1.csv", low_memory=False)
    cycle2_df = pd.read_csv("Observations/cycle2.csv", low_memory=False)

    # get the ids that intersect
    print("finding intersecting asteroids...")
    cycle1_df_unique = np.unique(cycle1_df["Original_Object_ID"])
    cycle2_df_unique = np.unique(cycle2_df["Object_ID"])
    intersect_ids_df = np.intersect1d(cycle1_df_unique, cycle2_df_unique)

    # compute all results
    print("find cycle 1 results...")
    cycle1_results_df = find_cycle_asteroids_light_curve_fit(cycle1_df, "Original_Object_ID", 1)

    print("find cycle 2 results...")
    cycle2_results_df = find_cycle_asteroids_light_curve_fit(cycle2_df, "Object_ID", 2)

    print("comparing cycles...")
    combine_results_df = compare_cycles(cycle1_results_df, cycle2_results_df, intersect_ids_df)

    # convert dataframes to csv
    print("convert results to csv files...")
    cycle1_results_df.to_csv('cycle1_results.csv', index=False)
    cycle2_results_df.to_csv('cycle2_results.csv', index=False)
    combine_results_df.to_csv('combine_results.csv', index=False)


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

def find_cycle_asteroids_light_curve_fit(cycle_df, id_col_name, cycle_num):

    # initialize output df
    columns = ["cycle", "asteroid_id", "reduced_chi2", "peak_power", 
               "period_(hr)", "amplitude", "num_observations"]
    
    results_df = pd.DataFrame(columns=columns)

    # count = 0

    # group each asteroid by their object id
    asteroids = cycle_df.groupby(id_col_name)

    # plot each asteroid
    for object_id, asteroid in asteroids:

        asteroid_info = (asteroid, cycle_num, object_id)

        result = find_asteroid_light_curve(asteroid_info)

        # add data to the results dataframe
        results_df.loc[len(results_df)] = result

        # count += 1
        # if count >= 50:
        #     break

    return results_df

# calculates the chi2 value based on the observed, expected, and error values
def reduced_chi_square(observed, expected, error):

    chi2 = 0

    for observation in range(0, len(observed)):
        chi2 += ((observed[observation] - expected[observation]) ** 2) / error[observation]

    chi2 = chi2 / len(observed - 4)

    return chi2

# compares cycle1 and cycle2 and compares the amplitude and period of the sine curve
def compare_cycles(cycle1_df, cycle2_df, intersect_ids):

    columns = ["asteroid_id", "period_(hr)_1", "amplitude_1",    
               "period_(hr)_2", "amplitude_2"]
    results_df = pd.DataFrame(columns=columns)

    intersect_ids_df = pd.DataFrame(intersect_ids, columns=["asteroid_id"])

    for row in intersect_ids_df.itertuples(index=False):
        asteroid_id = row.asteroid_id

        row1 = cycle1_df[cycle1_df["asteroid_id"] == asteroid_id]
        row2 = cycle2_df[cycle2_df["asteroid_id"] == asteroid_id]

        if row1.empty or row2.empty:
            continue

        period1 = row1["period_(hr)"].values[0]
        amplitude1 = row1["amplitude"].values[0]
        period2 = row2["period_(hr)"].values[0]
        amplitude2 = row2["amplitude"].values[0]

        results_df.loc[len(results_df)] = [
            asteroid_id,
            period1,
            amplitude1,
            period2,
            amplitude2
        ]

    return results_df

# defines the sine function to fit on the light curve plot
def sine_function(x, amplitude, frequency, phase, offset):
    
    return amplitude * np.sin(frequency * x + phase) + offset

################################################################################
main()