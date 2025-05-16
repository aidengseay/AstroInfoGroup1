# Astroinformatics Bootcamp 2025
## Group 1 - Incorporation of TESS Data
### Project Overview
Goal: Identify interesting **lightcurves** algorithmically.
- Determine if there are any overlapping targets between Cycle 1 and Cycle 2. Compare these targets by their periods and amplitudes.

#

<p align="center"><img src="Images/tess.jpeg">

<p align="center"><i>TESS Telescope</i></p>

#

<p align="center"><img src="Images/Object3_lightcurve.png">

<p align="center"><i>Lightcurve for asteroid "Juno"</i></p>

#

### Code Workflow

#### Imports Used
Below are imports that were used across the entire GitHub repository. To get the same results the researcher may have to `pip install` a couple of packages: 
- `pandas`
- `numpy`
- `matplotlib.pyplot`
- `astropy`

#### Step 1: Download Tess Data from Mongo DB
The purpose of this is to download the data onto our local system to decrease program run time. From now on we can get the data from our system locally and not have to wait for MongoDB to respond.
- First cell in `GrabLightCurve/DownloadMongoDB.ipynb` defines a class in order to gain access to the database.
- The `config.ini` file will consist of the username, password, host name and port number.
- This program will take in cycle1 data and cycle2 data and insert it into a pandas data frame. Then the Pandas data frame will be turned into a csv.

#### Step 2: Fit Light Curve
The `GrabLightCurve/FitLightCurve.py` file is ran in Monsoon for collecting large amounts of data. `GrabLightCurve/FitLightCurveTesting.ipynb` is used for testing before stating on a much larger dataset. Both of these programs are nearly identical.
- **Note**: the only difference between these files is `FitLightCurve.py` takes in cmd arguments `python3 FitLightCurve.py [cores] [core_num]` This will allow the program to be run in multiple scripts on Monsoon to accelerate the computation time. Ex. You are running 10 scripts on Monsoon so you will call the program by `python3 FitLightCurve.py 10 0-9`. See the folder `GrabLightCurve/MonsoonScripts` for examples. The file `GenerateJobs.py` automates the creation of these scripts.
- For this program to work `Observations/cycle1.csv` and `Observations/cycle2.csv` need to be found in the same folder the script is in.

This program will iterate through each asteroid and complete the following:
- Create a periodogram based on time (in hours) and absolute magnitude.
- Find the peak power from the periodogram to get the best frequency and period (**Note:** Be sure to double the period).
- Use the frequency that had the peak power, compute a sine curve fit with a Lomb Scargle model.
- This program will output `cycle num, asteroid_id, reduced_chi2 peak_power, period_(hr), amplitude, num_observations` for each asteroid.

#### Step 3: Analyze and Filter Results
Below are the programs that analyze the data. This is where we get to do the science! Before we do the science though we need to do combine all the data across each core into one file for analysis and filtering.
- The file `AnalyzeLightCurve/CombineMonsoonData.py` takes x amount of output files depending on x amount of scripts that were running on Monsoon and outputs data from each core into one file. For this program to work, the researcher must have a folder called `MonsoonDataReturn` holding all the output files from Monsoon. The program will return `cycle1_results.csv` and `cycle2_results.csv`.

Now that we have the data including `cycle num, asteroid_id, reduced_chi2 peak_power, period_(hr), amplitude, num_observations` from Monsoon, we can start filtering asteroids to find ones that are **interesting**.
- The file `AnalyzeLightCurve/FilterLightCurveData.ipynb` filters out asteroids that do not have ideal properties. For this program to work data must be in `Data/cycle1_results.csv` and `Data/cycle2_results.csv` in the same folder as this program. Below are the following filters used (throw out data that meets the following below):
    - Number of Observations < 100
    - Reduced Chi2 Value > 1.5
    - Peak Power < 0.4
    - Amplitude > 1

- The file `AnalyzeLightCurve/GetCycleIntersection.py` intersects both cycle 1 and cycle 2 data into a combined file for easier comparison. In order for this program to work the researcher needs to have `cycle1_results.csv` and `cycle2 results.csv` in the same folder as this program. This will output a file name `cycle_both_results.csv`. This is very similar to `AnalyzeLightCurve/GetCycleIntersectionDetailed.py` which makes a combined csv that is more detailed with all the data collected.

In one week this was able to cut down the number of asteroids to look at down significantly. We used `GrabLightCurve/QueueSingleAsteroid.ipynb` to look at each asteroid individually to find interesting characteristics.
    

#### Other Code Tools

##### Queue Single Asteroid
The file `GrabLightCurve/QueueSingleAsteroid.ipynb` is similar to `FitLightCurve.py`. These files have the same requirements for input but `QueueSingleAsteroid.ipynb` is used for a single asteroid and takes in a single asteroid id. This is really useful for testing specific cases when we filter down potential interesting asteroids.

##### Cycle Comparisons
The file `AnalyzeLightCurve/CycleComparisons.ipynb` is used to compare values including chi2 values, peak power values, period values, and
amplitude values. The purpose is to visually see the differences between cycle 1 and cycle 2.

##### Count Cycle Items
The file `GrabLightCurve/CountCycleItems.ipynb` was an initial testing file used to count how many asteroids were in each cycle. This also determined how many asteroids where in both cycles. Like `FitLightCurve.py`, `Observations/cycle1.csv` and `Observations/cycle2.csv` must be in the same directory for this program to work.

##### Magnitude Error Test
The file `GrabLightCurve/MagnitudeErrorTest.ipynb` was also an initial testing file used to plot the apparent magnitude with time also tracking the date for a specific asteroid. Like `GrabLightCurve/DownloadMongoDB.ipynb`, the `config.ini` needs to be in the same folder as this program for it to run properly.