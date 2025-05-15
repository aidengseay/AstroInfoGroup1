#!/bin/bash
#SBATCH --job-name=find_light_curve0                 # the name of your job
#SBATCH --output=/scratch/ags392/curve_out0.txt      # this is the file your output and errors go to
#SBATCH --error=/scratch/ags392/curve_out0.err       # this is the file your output and errors go to
#SBATCH --chdir=/scratch/ags392                        # your work directory
#SBATCH --time=5:00:00                                  # (max time) 5 hrs
#SBATCH --mem=10000                                     # (total mem) 10GB of memory

module load anaconda3
conda activate astro_info
python3 -u FitLightCurve.py 10 0
echo "FitLightCurve.py finished successfully."
