#!/usr/bin/env python
# coding: utf-8

import argparse
import sys

#GOAL: Use pandas to import state energy production data into dataframe
#NOTE: This dataset has some consumption metrics in it too! -MM :) 10.30.2019
#Then perform transformations needed 
def main():
    import pandas as pd
    import numpy as np
    import csv
    import xlrd 
    import urllib
    import os

    #NOTE: Link active as of 10.31.2019
    link = 'https://www.eia.gov/state/seds/sep_prod/xls/Prod_dataset.xlsx'

    #Initialize an empty dataframe 
    data2 = pd.DataFrame()

    #Pull in the header
    energy = pd.read_excel(link, sheet_name=0, header=0)

    #Remove the US, X3, and X5 rows from energy df
    badstates = ['US', 'X3', 'X5']
    energy_states = pd.DataFrame()
    energy_states = energy[~energy.StateCode.isin(badstates)]

    #Initialize an empty dataframe, that we will build up
    energy_v1 = pd.DataFrame()

    #YEARS
    #Get years from the headers, then repeat the years, and turn into a series
    #Start by extracting a list of all headers, called list_col
    list_col = []
    for col in energy_states.columns: 
        list_col.append(col)

    #Extract list of years from header
    list_years = list_col[3:]

    #List containing repeating statecodes
    list_statecodes_rp = energy_states[energy_states.columns[1]]
    #Number of unique states
    list_statecodes = list(set(list_statecodes_rp))

    #Number of unique categories
    list_categories_rp0 = energy_states[energy_states.columns[2]]
    list_categories = list(set(list_categories_rp0))

    #Repeat each 'Year' from the list, by the number of states (51)
    list_years_rp = []
    for i in range(len(list_statecodes)):
        list_years_rp.extend(list_years)

    #turn the list_years_repeated into a series
    series_years_rp = pd.Series(list_years_rp)

    #Insert years_rp into new dataframe
    energy_v1.insert(0, 'Years', series_years_rp)

    #STATE CODES
    #List containing repeating statecodes
    list_statecodes_rp = energy_states[energy_states.columns[1]]

    #Remove the duplicate statecodes, and preserve order
    tracker = set()
    list_statecodes = []
    for item in list_statecodes_rp:
        if item not in tracker:
            tracker.add(item)
            list_statecodes.append(item)

    #Extract list of years from header
    list_years = list_col[3:]

    #Repeat each 'State_Code' from the list, for the number of years (list comprehension)
    list_statecodes_rp2 = [statecode for statecode in list_statecodes for i in range(len(list_years))]

    #Turn the list of repeated statecodes into a series
    series_statecodes_rp2 = pd.Series(list_statecodes_rp2)

    #Insert statecodes_rp2 into new dataframe (USE THIS)
    energy_v1.insert(1, 'State_Code', series_statecodes_rp2)

    #VALUES - ENERGY PRODUCTION
    #First select array that only has values, no headers other than 'Year'
    energy_values = pd.DataFrame()
    energy_values = energy_states.iloc[:, 3:]
    energy_values = energy_values.transpose()

    #Remove the duplicate categories, and preserve order
    list_categories_rp0 = energy_states[energy_states.columns[2]]
    tracker = set()

    #This list will contain the unique category names
    list_categories = list()
    for item in list_categories_rp0:
        if item not in tracker:
            tracker.add(item)
            list_categories.append(item)

    def make_cat_list(col_index, list_categories):
        #INPUT: Column header index, representing Energy Production/Consumption Category 
        
        #OUTPUT: Series of rows for said column header, inputted into dataframe 
        
        #Make a copy of the col_index, to be used later
        col_index_copy = col_index
        list_stateyearcat = list()
        
        #Build up your category values list with the while loop
        while col_index < len(energy_values.columns):
            list_stateyearcat.extend(energy_values[energy_values.columns[col_index]])
            col_index += len(list_categories)

        #Turn the list of category values into a series
        series_stateyearcat = pd.Series(list_stateyearcat)
        
        #Get the category name
        cat_name = list_categories[col_index_copy]
        
        #Calculate which dataframe col_pos to insert your series into
        col_pos = 2 + col_index_copy
        
        #Insert your series, it's name, and position into the dataframe
        energy_v1.insert(col_pos, cat_name, series_stateyearcat)

    #Perform the make_cat_list function for each category header 
    #Number of categories 
    for i in range(len(list_categories)):
        make_cat_list(i, list_categories)

    #NAVIGATE TO THE /data folder
    os.chdir("..")
    os.chdir('data')

    #Output the dataframe to a csv file
    export_csv = energy_v1.to_csv('EIA_State_Production_1960-2017_clean.csv', index = None, header=True)

    #NAVIGATE BACK TO THE /src folder
    os.chdir("..")
    os.chdir('src')

if __name__ == '__main__':
    print(f"We're in file {__file__}")
    print("Calling energyprod_cleaning.py -> main() ")
    main()