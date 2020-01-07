#!/usr/bin/env python
# coding: utf-8

import argparse
import sys

#GOAL: Use the Bureau of Economic Analysis (BEA) API to get personal income, population,
# and per capita income data, add statecode column, and then output to a csv file

def main():
    import pandas as pd
    import requests
    import xml.etree.ElementTree as et 
    import re
    import os

    #YOUR BEA API KEY HERE
    #Get your own api key at this link: https://apps.bea.gov/API/signup/index.cfm
    #BEA api user guide: https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf
    bea_api_key = 'B43EF31E-75BB-4593-A82D-AB4816CEFFB9'

    #Real GDP for all states, all years, in XML format
    # https://apps.bea.gov/api/data/?UserID={bea_api_key}
    # &method=GetData
    # &datasetname=Regional
    # &TableName=SAGDP9N
    # &LineCode=1
    # &Year=2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016
    # &GeoFips=STATE
    # &ResultFormat=xml

    #Personal income, population, and per capita income by state (1997-)
    #Hard-coding some API elements
    GDP_Table = 'SAINC1'
    Years = '2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016'
    GeoFips_States = '01000,02000,04000,05000,06000,08000,09000,10000,11000,12000,13000,15000,16000,17000,18000,19000,20000,21000,22000,23000,24000,25000,26000,27000,28000,29000,30000,31000,32000,33000,34000,35000,36000,37000,38000,39000,40000,41000,42000,44000,45000,46000,47000,48000,49000,50000,51000,53000,54000,55000,56000'
    Linecode_list = [1,2,3]

    #PERSONAL INCOME
    #Get Personal income for all states, from years 2000-2016, in xml format
    api_url = f'https://apps.bea.gov/api/data/?UserID={bea_api_key}&method=GetData&datasetname=Regional&TableName={GDP_Table}&LineCode={Linecode_list[0]}&Year={Years}&GeoFips={GeoFips_States}&ResultFormat=xml'
    r = requests.get(api_url)

    #Turns the xml response into ElementTree root
    root = et.fromstring(r.content)

    df_cols = ["Year", "State", "Personal Income (millions)"]
    rows = []

    #For each row of data in the xml response, capture the tags and output to rows
    for child in root.iter('Data'):
        year = child.attrib.get("TimePeriod")
        state = child.attrib.get("GeoName")
        income = child.attrib.get("DataValue")
        income2 = float(re.sub('[,]', '', income))
        rows.append({"Year": year, "State": state, 
                     "Personal Income (millions)": income2})
    out_df = pd.DataFrame(rows, columns = df_cols)

    #POPULATION
    #Get Population for all states, from years 2000-2016, in xml format
    api_url = f'https://apps.bea.gov/api/data/?UserID={bea_api_key}&method=GetData&datasetname=Regional&TableName={GDP_Table}&LineCode={Linecode_list[1]}&Year={Years}&GeoFips={GeoFips_States}&ResultFormat=xml'
    r2 = requests.get(api_url)

    #Turns the xml response into ElementTree root
    root2 = et.fromstring(r2.content)

    df_cols = ["Year", "State", "Population"]
    rows = []

    #For each row of data in the xml response, capture the tags and output to rows
    for child in root2.iter('Data'):
        year = child.attrib.get("TimePeriod")
        state = child.attrib.get("GeoName")
        population = child.attrib.get("DataValue")
        population2 = float(re.sub('[,]', '', population))
        rows.append({"Year": year, "State": state, 
                     "Population": population2})  
    out_df2 = pd.DataFrame(rows, columns = df_cols)

    #Merge the population column on the pre-existing table containing personal income
    results = out_df.merge(out_df2, how='left', left_on=['State', 'Year'], right_on=['State', 'Year'])

    #PER CAPITA INCOME
    #Get Per Capita Income for all states, from years 2000-2016, in xml format
    api_url = f'https://apps.bea.gov/api/data/?UserID={bea_api_key}&method=GetData&datasetname=Regional&TableName={GDP_Table}&LineCode={Linecode_list[2]}&Year={Years}&GeoFips={GeoFips_States}&ResultFormat=xml'
    r3 = requests.get(api_url)

    #Turns the xml response into ElementTree root
    root3 = et.fromstring(r3.content)
    rows1 = []

    #For each row of data in the xml response, capture the 'per capita income'
    for child in root3.iter('Data'):
        percap_income = child.attrib.get("DataValue")
        percap_income2 = float(re.sub('[,]', '', percap_income))
        rows1.append(percap_income2)
    results.insert(4, 'Per capita income (dollars)', rows1)

    #STATE CLEANING
    states_v1 = results['State'].tolist()
    states_v2 = []
    for state in states_v1:
        states_v2.append(re.sub('[*]', '', state))

    #Delete the unclean states column from dataframe
    del results['State']

    results.insert(4, 'State', states_v2)

    #STATE CODES
    #NOTE: Link active as of 11.4.2019
    url = 'https://raw.githubusercontent.com/mann-brinson/INF550_Emissions_Project/master/statecodes.csv'

    states = pd.read_csv(url)

    #Join the state codes on the pre-existing table
    results2 = results.merge(states,on='State')

    #NAVIGATE TO THE /data folder
    os.chdir("..")
    os.chdir('data')

    #Output the dataframe to a csv file
    export_csv = results2.to_csv('BEA_State_IncomePop_2000-2016_clean.csv', index = None, header=True)

    #NAVIGATE BACK TO THE /src folder
    os.chdir("..")
    os.chdir('src')

if __name__ == '__main__':
    print(f"We're in file {__file__}")
    print("Calling incomepop_cleaning.py -> main() ")
    main()