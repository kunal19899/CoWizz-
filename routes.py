from flask import render_template, redirect, request, url_for, session, flash
import requests
from datetime import datetime, timedelta
from flask import Flask
from v3 import app
from v3 import static
import csv
from v3.feature_graph import main

@app.route("/")
def index():
    states = load_states()
    features = load_features()
    return render_template("index.html", states = states, features = features, stateData='', link = '', 
                            statePreview='', f1='', f2='', stateList = [])

@app.route("/animate", methods=['POST'])
def animate():
    ################ complete animate function to parse input here ##############
    states = load_states()
    features = load_features()
    stateList = []
    abbrList = []
    if request.method == "POST":
        ipt = request.form
        for item in ipt:
            if item != 'feature1':
                stateList.append(ipt[item])
                abbrList.append(states[ipt[item]])
            else: break
        # main(stateList, ipt['feature1'], ipt['feature2'])
        feature1 = ipt['feature1']
        feature2 = ipt['feature2']
        statePreview = ', '.join(stateList)
        stateData = load_states_data(abbrList)
    return render_template('index.html', states=states, features=features, stateData = stateData, link = 'active', 
                            statePreview=statePreview, f1=feature1, f2=feature2, stateList=stateList)
    #############################################################################


def load_states():
    states_names = {}
    with open('v3/static/states.csv') as states:
        states_map = csv.reader(states, delimiter=',')
        for state, abbr in states_map:
            if state != "State":
                states_names[state] = abbr
    return states_names

def load_features():
    features_names = {}
    with open('v3/static/features.csv') as fp:
        features = csv.reader(fp, delimiter=',')
        for item, name in features:
            features_names[item] = name

    return features_names
    
def load_states_data(stateList):
    
    stateData=""
    for x in range(len(stateList)):    
        with open('v3/static/CDC-all-states.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            #print(stateList[x])
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
