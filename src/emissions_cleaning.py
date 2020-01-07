#!/usr/bin/env python
# coding: utf-8

import argparse
import sys

#GOAL: Use pandas to import state emissions data into dataframe
#Then perform transformations needed 

def main():
	import pandas as pd
	import numpy as np
	import os

	#NOTE: Link works as of 10.31.2019
	link = 'https://www.eia.gov/environment/emissions/state/excel/summary_2016.xlsx'
	xd = pd.read_excel(link, sheet_name=0, header=2)

	#Remove rows (top:bottom, left:right) that don't include data
	data = xd.iloc[:51, :28]

	#Initialize a second empty dataframe (USE THIS)
	data2 = pd.DataFrame()

	#YEARS
	#Get years from the headers, then repeat the years, and turn into a series
	#Start by extracting a list of all headers, called list_col
	list_col = []
	for col in data.columns: 
	    list_col.append(col)

	#Extract list of years from header
	list_years = list_col[1:]

	#Number of states
	list_statecodes = data[data.columns[0]]

	#Repeat each 'Year' from the list, for the number of states (51)
	list_years_rp = []
	for i in range(len(list_statecodes)):
	    list_years_rp.extend(list_years)

	#turn the list_years_repeated into a series
	series_years_rp = pd.Series(list_years_rp)

	#Insert years_rp into new dataframe (USE THIS)
	data2.insert(0, 'Years', series_years_rp)

	#STATES
	#Get the first column 'State' and turn it into a list (USE THIS)
	list_states = data[data.columns[0]]

	#Repeat each 'State' from the list, for the number of years V2 (list comprehension)
	list_states_rp = [state for state in list_states for i in range(len(list_years))]

	#Turn the list of repeated statecodes into a series
	series_states_rp = pd.Series(list_states_rp)

	#Insert states_rp into new dataframe (USE THIS)
	data2.insert(1, 'State', series_states_rp)

	#CO2 EMISSIONS

	#First select array that starts with State on the left, and grabs everything to right
	data_co2 = pd.DataFrame()
	data_co2 = data.iloc[:, 1:]
	data_co2 = data_co2.transpose()
	#Remove rows that are not the data (in this case, state)
	data_co2 = data_co2.iloc[:, :]

	#State-by-state, starting wit AL moving alphabetically, 
	#compile a list of per-state, per-year co2 emissions
	list_stateyearco2 = []
	for i in range(len(data_co2.columns)):
	    list_stateyearco2.extend(data_co2[data_co2.columns[i]])

	#Turn the list of per into a series
	series_stateyearco2 = pd.Series(list_stateyearco2)

	#Insert stateyearco2 into new dataframe (USE THIS)
	data2.insert(2, 'CO2_Emissions', series_stateyearco2)

	#NAVIGATE TO THE /data folder
	os.chdir("..")
	os.chdir('data')

	#Output the dataframe to a csv file
	export_csv = data2.to_csv ('EIA_State_CO2Emissions_2000-2016_clean.csv', index = None, header=True) 

	#NAVIGATE BACK TO THE /src folder
	os.chdir("..")
	os.chdir('src')

if __name__ == '__main__':
    print(f"We're in file {__file__}")
    print("Calling emissions_cleaning.py -> main() ")
    main()