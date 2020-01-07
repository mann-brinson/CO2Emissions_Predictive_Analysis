#!/usr/bin/env python
# coding: utf-8

import argparse
import sys

#GOAL: Make a decision tree to understand what 
# consumption type increases are associated with higher emissions 

def main():
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    from sklearn import tree
    from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
    from IPython.display import Image  
    from sklearn.tree import export_graphviz
    import pydotplus
    import os

    os.chdir("..")
    os.chdir('data')

    #Get data with columns: 
    # 1. -- Transportation Emissions
    emissions = pd.read_csv('EIA_State_CO2Emissions_2000-2016_clean.csv')

    # 2. -- Total energy consumption
    consumption = pd.read_csv('EIA_State_Consumption_1960-2017_clean.csv')

    #Add state codes to emissions table
    #STATE CODES
    #NOTE: Link active as of 11.4.2019
    url = 'https://raw.githubusercontent.com/mann-brinson/INF550_Emissions_Project/master/statecodes.csv'
    states = pd.read_csv(url)

    #put attributes in another table, and remove them
    emis_values = emissions.iloc[:, 2:]
    emissions.drop(emissions.columns[2:], axis=1, inplace=True)

    #Merge the statecodes onto the pre-existing table
    emissions_v2 = emissions.merge(states,on='State')

    #Then add the attributes back
    emis_final = emissions_v2.join(emis_values)

    #Do an inner join on the dataframes
    # Join emissions on consumption
    new_df1 = pd.merge(emis_final, consumption,  how='inner', left_on=['Years','State_Code'], right_on = ['Years','State_Code'])

    def get_1516_changes(statecode_list, new_df1):
        '''
        INPUT 1: A list of statecodes
        INPUT 2: A dataframe of Emissions & Consumption stats with one row per state, per year
        OUTPUT: A dict of one list per state, showing the state Emission & Consumption change results
        '''
        changes_1516_dict = {}
        for statecode in statecode_list:
            #Then filter the data to only show state rows
            new_df2 = new_df1.loc[new_df1['State_Code'] == statecode]
            
            #Now filter to only show years 2015 and 2016
            #Get the AL + 2015 row and convert to list
            emis_2015 = new_df2[new_df2['Years'].isin([2015])]
            emis_2015 = emis_2015.iloc[:, 3:]
            emis_2015_list = []

            # Iterate over each row 
            for index, rows in emis_2015.iterrows(): 
                # Create list for the current row 
                my_list =[rows.CO2_Emissions, rows.FFTCB, rows.NUETB, rows.RETCB] 
                # append the list to the final list 
                emis_2015_list.append(my_list) 

            #Get the 2016 row
            #Get the AL + 2016 row and convert to list
            emis_2016 = new_df2[new_df2['Years'].isin([2016])]
            emis_2016 = emis_2016.iloc[:, 3:]
            emis_2016_list = []

            # Iterate over each row 
            for index, rows in emis_2016.iterrows(): 
                # Create list for the current row 
                my_list =[rows.CO2_Emissions, rows.FFTCB, rows.NUETB, rows.RETCB] 
                # append the list to the final list 
                emis_2016_list.append(my_list) 
            
            # using list comprehension to find the changes  
            changes_1516 = [] 
            for i in range(len(emis_2016_list[0])): 
                changes_1516.append(emis_2016_list[0][i] - emis_2015_list[0][i])
            
            #If positive 2016-2015 diff, its an increase. if negative 2016-2015 diff, its a decrease
            changes_1516_f = []
            for i in changes_1516:
                if i > 0:
                    #Increase = 2
                    changes_1516_f.append(2)
                elif i < 0: 
                    #Decrease = 0
                    changes_1516_f.append(0)
                else:
                    #No change = 1
                    changes_1516_f.append(1)
            changes_1516_dict[statecode] = changes_1516_f
        return changes_1516_dict

    #Get a list of statecodes
    statecode_list = list(set(new_df1['State_Code'].tolist()))
    statecode_list.sort()

    #Testing the get_1516_changes function here
    changes_1516_dict = get_1516_changes(statecode_list, new_df1)

    #Convert the dict to a pandas df
    changes_1516_df = pd.DataFrame.from_dict(changes_1516_dict)
    changes_1516_df = changes_1516_df.transpose()
    changes_1516_df.columns = ['D_Emis','D_Fossil_Cons', 'D_Nuclear_Cons', 'D_Renew_Cons']

    #Get the target classifier (D_Emis) in a list
    #Take D_Emis_transport and turn into a list
    Y = changes_1516_df['D_Emis'].tolist()

    #Get the attributes (D_Fossil_Cons, D_Nuclear_Cons, D_Renew_Cons) in a list of lists
    X = []
    for index, row in changes_1516_df.iterrows():
        mylist = []
        mylist.append(row['D_Fossil_Cons'])
        mylist.append(row['D_Nuclear_Cons'])
        mylist.append(row['D_Renew_Cons'])
        X.append(mylist)

    #Run the decision tree algorithm 
    clf = tree.DecisionTreeClassifier(max_depth=3)
    model = clf.fit(X, Y)

    dot_data = export_graphviz(clf, out_file=None,  
                               filled=True, rounded=True,
                               special_characters=True,
                               feature_names=['D_Fossil_Cons', 'D_Nuclear_Cons', 'D_Renew_Cons'],
                               class_names=['Decrease', 'Increase'])

    graph = pydotplus.graph_from_dot_data(dot_data)  
    graph.write_png("decisiontree_emis_allfuels_A.png")

    #Get all combinations of two years
    year_list = list(set(new_df1['Years'].tolist()))

    startend_years_list = []
    for i in range(len(year_list)-1):
        year1 = year_list[i]
        year2 = year_list[i+1]
        startend_years = []
        startend_years.append(year1)
        startend_years.append(year2)
        startend_years_list.append(startend_years)
        
    #Get all combinations of years from 1990-2015
    year_list_9015 = list(set(new_df1['Years'].tolist()))
    year_list_9015.remove(2016)

    startend_years9015_list = []
    for i in range(len(year_list_9015)-1):
        year1 = year_list_9015[i]
        year2 = year_list_9015[i+1]
        startend_years = []
        startend_years.append(year1)
        startend_years.append(year2)
        startend_years9015_list.append(startend_years)

    def get_yr2yr1_changes(startend_years_list, statecode_list, new_df1):
        '''
        INPUT: startend_years_list - A list of sublists. Each sublist contains year1 and year2. Example: [2014, 2015], [2015, 2016]
        INPUT: statecode_list - A list of unique statecodes
        INPUT: A dataframe of Emissions & Consumption stats with one row per state, per year
        OUTPUT: A dict of one list per state, per year combination, showing the state Emission & Consumption change results
        '''
        changes_yr2yr1_dict = {}
        for startend_years in startend_years_list:
            year1 = startend_years[0]
            year2 = startend_years[1]
            for statecode in statecode_list:
                new_df2 = new_df1.loc[new_df1['State_Code'] == statecode]
                #Year 1
                emis_year1 = new_df2[new_df2['Years'].isin([year1])]
                emis_year1 = emis_year1.iloc[:, 3:]
                emis_year1_list = []
                for index, rows in emis_year1.iterrows(): 
                    my_list =[rows.CO2_Emissions, rows.FFTCB, rows.NUETB, rows.RETCB] 
                    emis_year1_list.append(my_list)
                #Year 2
                emis_year2 = new_df2[new_df2['Years'].isin([year2])]
                emis_year2 = emis_year2.iloc[:, 3:]
                emis_year2_list = []
                for index, rows in emis_year2.iterrows(): 
                    my_list =[rows.CO2_Emissions, rows.FFTCB, rows.NUETB, rows.RETCB] 
                    emis_year2_list.append(my_list) 

                # using list comprehension to find the changes  
                changes_list = [] 
                for i in range(len(emis_year2_list[0])): 
                    changes_list.append(emis_year2_list[0][i] - emis_year1_list[0][i])
                #If positive year2-year1 diff, its an increase. if negative year2-year1 diff, its a decrease
                changes_yr2yr1_f = []
                for i in changes_list:
                    if i > 0:
                        #Increase = 2
                        changes_yr2yr1_f.append(2)
                    elif i < 0: 
                        #Decrease = 0
                        changes_yr2yr1_f.append(0)
                    else:
                        #No change = 1
                        changes_yr2yr1_f.append(1)
                state_years = statecode + " '" + str(year1)[2:] + "-" +str(year2)[2:]
                changes_yr2yr1_dict[state_years] = changes_yr2yr1_f
        return changes_yr2yr1_dict

    #Testing the get_yr2yr1_changes function here
    changes_allyears_dict = get_yr2yr1_changes(startend_years9015_list, statecode_list, new_df1)

    #Convert the dict to a pandas df
    changes_allyears_df = pd.DataFrame.from_dict(changes_allyears_dict)
    changes_allyears_df = changes_allyears_df.transpose()
    changes_allyears_df.columns = ['D_Emis','D_Fossil_Cons', 'D_Nuclear_Cons', 'D_Renew_Cons']

    #Output the dataframe to a csv file
    export_csv = changes_allyears_df.to_csv ('decisiontree_emis_allfuels_B_data.csv', index = 1, header=True) 

    #Get the target classifier (D_Emis_transport) in a list
    #Take D_Emis_transport and turn into a list
    Y = changes_allyears_df['D_Emis'].tolist()

    #Get the attributes (D_Coal_Cons, D_NatGas_Cons, D_Petrol_Cons) in a list of lists
    X = []
    for index, row in changes_allyears_df.iterrows():
        mylist = []
        mylist.append(row['D_Fossil_Cons'])
        mylist.append(row['D_Nuclear_Cons'])
        mylist.append(row['D_Renew_Cons'])
        X.append(mylist)

    #Run the decision tree algorithm 
    clf = tree.DecisionTreeClassifier(max_depth=3)
    model = clf.fit(X, Y)

    dot_data = export_graphviz(clf, out_file=None,  
                               filled=True, rounded=True,
                               special_characters=True,
                               feature_names=['D_Fossil_Cons', 'D_Nuclear_Cons', 'D_Renew_Cons'],
                               class_names=['Decrease', 'Increase'])

    graph = pydotplus.graph_from_dot_data(dot_data)  
    graph.write_png("decisiontree_emis_allfuels_B.png")

    #Training and testing the decision tree
    #GOAL: Calculate the accuracy of the decision tree in predicting emissions increase status

    #STEP 1: Split the data into train and test. 
    # The training dataset will contain years 1990-2015. 
    # The test dataset will contain years 2015-2016. 

    #STEP 2: Train a decision tree with the X_train and Y_train data 
    #STEP 3: Test the decision tree with X_test, to get Y_pred
    #STEP 4: Compare the Y_pred with Y_actual, to get a true positive rate 

    #STEP 1: Split the data into train and test. 
    # The training dataset will contain years 1990-2015. 
    # The test dataset will contain years 2015-2016. 

    #GENERATE TRAINING DATA
    #Get a list of statecodes
    statecode_list = list(set(new_df1['State_Code'].tolist()))
    statecode_list.sort()

    #Get all combinations of years from 1990-2015
    year_list_9015 = list(set(new_df1['Years'].tolist()))
    year_list_9015.remove(2016)

    startend_years9015_list = []
    for i in range(len(year_list_9015)-1):
        year1 = year_list_9015[i]
        year2 = year_list_9015[i+1]
        startend_years = []
        startend_years.append(year1)
        startend_years.append(year2)
        startend_years9015_list.append(startend_years)

    #Training dataset: Gets changes from 1990-2015
    train_dict = get_yr2yr1_changes(startend_years9015_list, statecode_list, new_df1)

    #Convert the training_dict to a pd.dataframe
    train_df = pd.DataFrame.from_dict(train_dict)
    train_df = train_df.transpose()
    train_df.columns = ['D_Emis','D_Coal_Cons', 'D_NatGas_Cons', 'D_Petrol_Cons']
    #train_df.tail()

    X_train = train_df.drop("D_Emis", axis=1)
    Y_train = train_df["D_Emis"]

    #GENERATE TESTING DATA
    year_list_1516 = [2015, 2016]
    startend_years1516_list = [[2015, 2016]]

    #Test dataset: Gets changes from 2015-2016
    test_dict = get_yr2yr1_changes(startend_years1516_list, statecode_list, new_df1)
    test_df = pd.DataFrame.from_dict(test_dict)
    test_df = test_df.transpose()
    test_df.columns = ['D_Emis','D_Coal_Cons', 'D_NatGas_Cons', 'D_Petrol_Cons']

    X_test = test_df.drop("D_Emis", axis=1)
    Y_actual = test_df["D_Emis"]

    #STEP 2: Train a decision tree with the X_train and Y_train data 
    decision_tree = tree.DecisionTreeClassifier(max_depth=3)
    decision_tree.fit(X_train, Y_train) 

    #STEP 3: Test the decision tree with X_test, to get Y_pred
    Y_pred = decision_tree.predict(X_test) 

    #STEP 4: Compare the Y_pred with Y_actual, to get a true positive rate 
    print("Emisissions vs All Fuels Decision Tree Accuracy:",metrics.accuracy_score(Y_actual, Y_pred))

    os.chdir("..")
    os.chdir('src')

if __name__ == '__main__':
    print(f"We're in file {__file__}")
    print("Calling decisiontree_emis_allfuels.py -> main() ")
    main()


