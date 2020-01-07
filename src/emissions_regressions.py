#!/usr/bin/env python
# coding: utf-8

import argparse
import sys

#GOAL: Find basic regressions for the below
def main():
	import numpy as np
	import matplotlib.pyplot as plt
	import pandas as pd
	from sklearn.linear_model import LinearRegression
	import os

	os.chdir("..")
	os.chdir('data')

	#Get data with columns: 
	# 1. -- Transportation Emissions
	data1 = pd.read_csv('EIA_State_CO2Emissions_all_sectors_1980-2016_clean.csv')

	# 2. -- Real GDP
	data2 = pd.read_csv('BEA_State_RealGDP_2000-2016_clean.csv')

	# 3A. -- Population
	# 3B. -- Total personal income 
	data3 = pd.read_csv('BEA_State_IncomePop_2000-2016_clean.csv')

	# 4. -- Total energy consumption
	data4 = pd.read_csv('EIA_State_Production_1960-2017_clean.csv')

	#Do an inner join on all of the dataframes
	#ARTICLE: https://stackoverflow.com/questions/41815079/pandas-merge-join-two-data-frames-on-multiple-columns

	# STEP 1. Join Real GDP (data2) on Transportation Emissions (data1)
	# Transportation Emissions (data1) : {# 'Years' - column 1,'State' - column 2, 'CO2_Emissions_transportation' - column 7}
	# Real GDP (data2) : {'Years' - column 1, 'State' - column 2, 'Real_GDP' - column 3}

	new_df1 = pd.merge(data1, data2,  how='inner', left_on=['Years','State'], right_on = ['Year','State'])

	# STEP 2 : Join PopIncome (data3) on the larger joined data (new_df1)
	# PopIncome (data3) : {'Population_persons' - column 4, 'Years' - column 1, 'State_Code' - column 2, 'Personal_income_millions' - column 3}

	#JOIN
	new_df2 = pd.merge(new_df1, data3,  how='inner', left_on=['Years','State'], right_on = ['Year','State'])

	# STEP 3. Join EnergyProduction (data4) on larger joined data (new_df2)
	# EnergyProduction (data4) : {'TETCB' - column index -6, 'Years' - column 1, 'State_Code' - column 2}
	#JOIN
	new_df3 = pd.merge(new_df2, data4,  how='inner', left_on=['Years','State_Code_x'], right_on = ['Years','State_Code'])

	#Output the dataframe to csv, to review
	export_csv = new_df3.to_csv ('Master_Dataset_clean.csv', index = None, header=True) 

	#Then filter the data to only show 2016 rows
	new_df3 = new_df3.loc[new_df3['Years'] == 2016]

	#Then filter out the outliers (NY, CA, TX)
	outliers = ['NY', 'CA', 'TX']
	new_df3 = new_df3[~new_df3['State_Code'].isin(outliers)]

	# QUESTION 1: Regress Real GDP on Transportation Emissions
	# What is R^2 ? 
	X1 = new_df3.iloc[:, 8].values.reshape(-1, 1) # Real_GDP: values converts it into a numpy array
	Y = new_df3.iloc[:, 6].values.reshape(-1, 1) # CO2Emis_transport: -1 means that calculate the dimension of rows, but have 1 column

	#Instantiate a LinearRegression object
	linear_regressor = LinearRegression()

	linear_regressor.fit(X1, Y)
	#print(linear_regressor.get_params())

	#Result is a np array of predicted y values
	Y_pred = linear_regressor.predict(X1)

	#Result is the score R^2 after passing the arrays for X & Y
	print('Regression 1: R^2 =', round(linear_regressor.score(X1, Y), 4))

	#Plot the regression line
	fig = plt.figure()
	#plt.subplots_adjust(top=2) #If you enable this, it won't save the png properly
	ax1 = fig.add_subplot(211)
	ax1.set_xlabel('2016 State Real GDP (m dollars)')
	ax1.set_ylabel('CO2 Emissions (m metric tons)')
	ax1.set_title('2016 State Real GDP & Transportation Emissions')
	fig = plt.scatter(X1, Y)
	plt.plot(X1, Y_pred, color='red')

	plt.savefig('regression1.png', dpi=100)

	# QUESTION 2: Regress Population on Transportation Emissions
	# What is R^2 ? 
	X2 = new_df3.iloc[:, 13].values.reshape(-1, 1) # Population: values converts it into a numpy array
	Y = new_df3.iloc[:, 6].values.reshape(-1, 1) # CO2Emis_transport: -1 means that calculate the dimension of rows, but have 1 column

	#Instantiate a LinearRegression object
	linear_regressor = LinearRegression()

	linear_regressor.fit(X2, Y)

	#Result is a np array of predicted y values
	Y_pred = linear_regressor.predict(X2)

	#Result is the score R^2 after passing the arrays for X & Y
	print('Regression 2: R^2 =', round(linear_regressor.score(X2, Y), 4))

	#Plot the regression line
	fig = plt.figure()
	#fig.subplots_adjust(top=2) #If you enable this, it won't save the png properly
	ax1 = fig.add_subplot(211)
	ax1.set_xlabel('2016 State Population (10m persons)')
	ax1.set_ylabel('CO2 Emissions (m metric tons)')
	ax1.set_title('2016 State Population & Transportation Emissions')
	fig = plt.scatter(X2, Y)
	plt.plot(X2, Y_pred, color='red')

	plt.savefig('regression2.png', dpi=100)

	# QUESTION 3: Regress Total Personal Income on Transportation Emissions
	# What is R^2 ? 
	X3 = new_df3.iloc[:, 12].values.reshape(-1, 1) # Income: values converts it into a numpy array
	Y = new_df3.iloc[:, 6].values.reshape(-1, 1) # CO2Emis_transport: -1 means that calculate the dimension of rows, but have 1 column

	#Instantiate a LinearRegression object
	linear_regressor = LinearRegression()

	linear_regressor.fit(X3, Y)

	#Result is a np array of predicted y values
	Y_pred = linear_regressor.predict(X3)

	#Result is the score R^2 after passing the arrays for X & Y
	print('Regression 3: R^2 =', round(linear_regressor.score(X3, Y), 4))

	#Plot the regression line
	fig = plt.figure()
	#fig.subplots_adjust(top=2)
	ax1 = fig.add_subplot(211)
	ax1.set_xlabel('2016 State Income (m current dollars)')
	ax1.set_ylabel('CO2 Emissions (m metric tons)')
	ax1.set_title('2016 State Income & Transportation Emissions')
	fig = plt.scatter(X3, Y)
	plt.plot(X3, Y_pred, color='red')

	plt.savefig('regression3.png', dpi=100)

	# QUESTION 4: Regress Total Energy Consumption on Transportation Emissions
	# What is R^2 ? 
	X4 = new_df3.iloc[:, -6].values.reshape(-1, 1) # Energy_Consumption: values converts it into a numpy array
	Y = new_df3.iloc[:, 6].values.reshape(-1, 1) # CO2Emis_transport: -1 means that calculate the dimension of rows, but have 1 column

	#Instantiate a LinearRegression object
	linear_regressor = LinearRegression()

	linear_regressor.fit(X4, Y)

	#Result is a np array of predicted y values
	Y_pred = linear_regressor.predict(X4)

	#Result is the score R^2 after passing the arrays for X & Y
	print('Regression 4: R^2 =', round(linear_regressor.score(X4, Y), 4))

	#Plot the regression line
	fig = plt.figure()
	#fig.subplots_adjust(top=2)
	ax1 = fig.add_subplot(211)
	ax1.set_xlabel('2016 Energy Consumption (b btu)')
	ax1.set_ylabel('CO2 Emissions (m metric tons)')
	ax1.set_title('2016 Energy Consumption & Transportation Emissions')
	plt.scatter(X4, Y)
	plt.plot(X4, Y_pred, color='red')

	plt.savefig('regression4.png', dpi=100)

	os.chdir("..")
	os.chdir('src')

if __name__ == '__main__':
    print(f"We're in file {__file__}")
    print("Calling emissions_regressions.py -> main() ")
    main()