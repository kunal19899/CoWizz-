# Packages required for current version of the project
from flask import render_template, redirect, request, url_for, session, flash
import requests
from datetime import datetime, timedelta
from flask import Flask
from v3 import app
from v3 import static
import csv
from v3.feature_graph import main
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import STAP

# FUNCTION RUNS WHEN THE BASE HOST IS CALLED WITH THE '/' EXTENTION, e.g. https://localhost:5000/
@app.route("/")
def index():
    states = load_states() # load the states.csv file into this dict variable | format: {state: abbreviation}
    features = load_features() # loads the feature in to this dict variable | format: {feature id: feature name}

    # load 'index.html' with the following variables (loaded, empty): loaded - states, features; empty - stateData, link, statePreview, f1, f2, stateList
    return render_template("index.html", states = states, features = features, stateData='', link = '', 
        statePreview='', f1='', f2='', stateList = [])


# FUNCTION RUNS WHEN THE BASE HOST IS CALLED WITH THE '/animate' EXTENTION, e.g. https://localhost:5000/animate
# needs to be called with POST API method and data is required when being called
# called within the dashboard after submit button is clicked, cannot be called through the URL without data
@app.route("/animate", methods=['POST'])
def animate():
    states = load_states() # load the states.csv file into this dict variable | format: {state: abbreviation}

    features = load_features() # loads the feature in to this dict variable | format: {feature id: feature name}

    stateList = [] # initialize stateList as an empty list; will contain the states (full name) which the user(s) selected to view

    stateData = '' # initialize stateData as an empty string; will contain a string of CDC information

    abbrList = [] # initialize abbrList as an empty list; will contain the states (abbreviations) which the user(s) selected to view

    base = importr('base') # import Rs base packages

    # called if function called with POST API
    if request.method == "POST":
        ipt = request.form  # put the data into ipt (easier to call the information later in the code), 
                            # format: { allstates: all abbreviations, 'feature1': feature1, 'feature2': feature2}
        
        # loops through all the states which have been submitted (1 - 5) and the feature 
        for item in ipt:

            # since features in input and feature1 and feature2 at the end of the input dict, if else statement ends the loop after all the states have been read
            if item != 'feature1':

                stateList.append(ipt[item]) # state full name appended to stateList

                abbrList.append(states[ipt[item]]) # state abbreviation appended to abbrList

            else: break
             
        feature1 = ipt['feature1'] # feature1 contains feature1 info | format: {feature id: feature name}

        feature2 = ipt['feature2'] # feature2 contains feature2 info | format: {feature id: feature name}
       
        # reads the 'feature_graph_v4.R' file and stores the information into 'string'
        with open('/Users/kunalsamant/Documents/UTA/ITLab/COVID-19 visualisation/v3/feature_graph_v4.R', 'r') as f:
            string = f.read()

        compute = STAP(string, "main") # stores the information for the 'main' function in 'feature_graph_v4.R' in variable 'main'

        result1 = compute.main(stateList, feature1, feature2) # calls the 'main' function with appropriate arguments | compute.main() ==> variable.function_name()


        # reads the 'user_states_graph_fix.R' file and stores the information into 'string'
        with open('/Users/kunalsamant/Documents/UTA/ITLab/COVID-19 visualisation/v3/user_states_graph_fix.R', 'r') as f:
            string = f.read()
        
        display = STAP(string, "main") # stores the information for the 'main' function in ''user_states_graph_fix.R' in variable 'display'

        result2 = display.main(features[feature1], features[feature2]) # calls the 'main' function with appropriate arguments | display.main() ==> variable.function_name()
        
        statePreview = ', '.join(stateList) # creates a string of all the state names joined together with a ', ' to display
        
        
        # stateData = load_states_data(abbrList)

    # load 'index.html' with the following variables (loaded, empty): loaded - states, features, stateData, link, statePreview, f1, f2, stateList; no empty
    return render_template('index.html', states=states, features=features, stateData = stateData, link = 'active', 
                            statePreview=statePreview, f1=feature1, f2=feature2, stateList=stateList)


# HELPER FUNCTION:
# FUNCTION PARSES states.csv AND STORES INFORMATION
# RETURNS {state name: state abbreviation} for all states
def load_states():
    states_names = {} # initialize the dict

    # reads 'states.csv'
    with open('v3/static/states.csv') as states:
        states_map = csv.reader(states, delimiter=',') # parses 'states.csv'

        # loops over each state info to remove first line
        for state, abbr in states_map:
            if state != "State":
                states_names[state] = abbr
    return states_names


# HELPER FUNCTION:
# FUNCTION PARSES features.csv AND STORES INFORMATION
# RETURNS {feature id: feature name} for all features
def load_features():
    features_names = {} # initialize the dict

    # reads 'features.csv'
    with open('v3/static/features.csv') as fp:
        features = csv.reader(fp, delimiter=',') # parses 'features.csv'

        # loops over each feature info
        for item, name in features:
            features_names[item] = name

    return features_names
    
def load_states_data(stateList):
    
    stateData=""
    for x in range(len(stateList)):    
        with open('v3/static/CDC-all-states.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            deaths=0
            cases=0
            for row in reader:
                if(row['state']==stateList[x]):
                    deaths=deaths+int(row['deathIncrease'])
                    cases=cases+int(row['positiveIncrease'])
            stateData=stateData+stateList[x]+": Cases: "+str(f'{cases:,}')+", Deaths: "+str(f'{deaths:,}')+"|| ";           
    return stateData
          

# api functions beyond this point

if __name__ == "__main__":
    app.run( debug=True)
