# Astroinformatics Bootcamp 2025
## Group 1 - Incorporation of TESS Data
### Project Overview
- Goal: identify interesting **lightcurves** algorithmically
- Determine if there are any overlapping targets between Cycle 1 and Cycle 2. Compare these targets by their periods and amplitudes.

### Code Workflow

#### Step 1: Download Tess Data from Mongo DB
- First cell defines a class in order to gain access to the database
- The `config.ini` file will consist of the username, password, host name and port number.
- This program will take in cycle1 data and cycle2 data and insert it into a pandas data frame. Then the Pandas data frame will be turned into a csv.
- The purpose of this is to download the data onto our local system to decrease program run time.

#### Step 2: Fit Light Curve
- The `FitLightCurve.py` file is ran in Monsoon for collecting large amounts of data. `FitLightCurveTesting.ipynb` is used for testing before stating on a much larger dataset. Both of these programs are nearly identical.
    - **Note**: the only difference between these files is `FitLightCurve.py` takes in cmd arguments `python3 FitLightCurve.py [cores] [core_num]` This will allow the program to be run in multiple scripts on Monsoon to accelerate the computation time. Ex. You are running 10 scripts on Monsoon so you will call the program by `python3 FitLightCurve.py 10 0-9`. See the folder `GrabLightCurve/MonsoonScripts` for examples. The file `GenerateJobs.py` automates the creation of these scripts.
- For this program to work `Observations/cycle1.csv` and `Observations/cycle2.csv` need to be found in the same folder the script is in.
- This program will iterate through each asteroid and complete the following:
    - Create a periodogram based on time (in hours) and absolute magnitude.
    - Find the peak power from the periodogram to get the best frequency and period (**Note:** Be sure to double the period).
    - Use the frequency that had the peak power, compute a sine curve fit with a Lomb Scargle model.
    - This program will output `cycle num, asteroid_id, reduced_chi2 peak_power, period_(hr), amplitude, num_observations` for each asteroid.

#### Step 3: Analyze and Filter Results
- 




### Other Code Tools

#### Queue Single Asteroid
- The file `QueueSingleAsteroid.ipynb` is similar to `FitLightCurve.py`. These files have the same requirements for input but `QueueSingleAsteroid.ipynb` is used for a single asteroid and takes in a single asteroid id. This is really useful for testing specific cases.