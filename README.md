aaf -August 23, 2025
This is an archive of a copied version of ESMplot linked to AJT's git repo ESMplot 
(commit hash eee89b76550ce547f638516f1ba3f7358905608c with additional edits)

# ESMplot

Welcome to ESMplot: the Earth System Model plotting package on Python! <br/>
Author: Alex Thompson (ajthompson@wustl.edu) <br/>
Latest Update: 2024-04-17 <br/>
<br/>
This is the beta version of ESMplot, a Python package designed for flexible visualization of Earth system model netCDF output. 

# Installation
For current prototype version, download entire directory 'ESMplot' (size: ~55MB) from GitHub and place in your own working directory.

One way to do this is to run this line of code while in your own working directory: <br/>
```git clone https://github.com/alexjt28/ESMplot.git```

# Conda environment
Use /conda_envs/environment_ESMplot_py310.yml to create a conda environment with python 3.10 to run this package.<br/>

With 'environment_ESMplot_py310.yml' in your working directory, type "conda env create -f environment_ESMplot_py310.yml"<br/>

Then type "conda activate ESMplot_py3.10" to activate the conda environment.<br/>

NOTE: ESMplot currently requires Python version 3.10 to run properly.<br/>

# Table of Contents

============================== <br/>
directory **conda_envs** <br/>
============================== <br/>

Contains 'environment_ESMplot_py310.yml' file for creating a conda environment from which to run ESMplot

============================== <br/>
directory **examples** <br/>
============================== <br/>

Example scripts that show how to make plots with ESMplot. Included are calculate_seasavg.py (calculate seasonal average), calculate_seascyc.py (calculate seasonal cycle), and calculate_watertags.py (calculate water tagging results).

Note: when changing central_longitude for water tagging plots, use tagged_regions_cenlon0.py or tagged_regions_cenlon180.py first and then copy the desired file to tagged_regions.py

============================== <br/>
directory **ESMplot** <br/>
============================== <br/>

Directory storing source code for ESMplot.

============================== <br/>
directory **pdfs** <br/>
============================== <br/>

Directory used for storing output files. 
