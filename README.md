# Predictive Analysis of State CO2 Emissions  
INF 550 Emissions Project

**USER GUIDE**

**DESCRIPTION:** This application will create and run machine-learning models against US state emissions, economic, energy production, and energy consumption tables to predict future emissions. This project was based off of an assignment for USC INF 550 in Fall 2019 - Data Science at Scale, advised by Prof. Seon Ho Kim. 

**HOW TO RUN THE PYTHON APPLICATION**

STEP 1: Install Anaconda Python 3.7
	Link: https://www.anaconda.com/distribution/

STEP 2: Download the zip file 'Emissions_DataAnalysis.zip' locally

STEP 3: Within your terminal, navigate to the repository

STEP 4: Install the required python modules with the following command

```$ pip install --user --requirement REQUIREMENTS.txt```

STEP 5: Install GraphViz using the following command 

```$ conda install python-graphviz```
	
STEP 4: Run the program with the following command options 
```
$ python3 Emissions_DataAnalysis.py local
$ python3 Emissions_DataAnalysis.py remote
```

**LOCAL AND REMOTE OPTIONS**

**local** - runs the program with the local csv files provided in the repository. If the local csv files are not present, you will need to run the program remotely, to generate a local set of csvs before the analysis (aka machine-learning models) can be completed. 

**remote** - runs the program after first creating local, cleaned csv files from remote web sources included in the '...cleaning.py' files
