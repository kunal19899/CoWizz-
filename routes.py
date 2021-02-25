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
    return render_template("index.html", states = states, features = features, stateData='', link = '')

@app.route("/animate", methods=['POST'])
def animate():
    ################ complete animate function to parse input here ##############
    stateList=[]
    states = load_states()
    features = load_features()    
    print(request.form)
    if request.method == "POST":
        ipt = request.form        
        for item in ipt:
            if item != 'feature1':
                stateList.append(ipt[item])
            else: break
        stateData=load_states_data(stateList)        
        main(stateList, ipt['feature1'], ipt['feature2'])
    return render_template('index.html', states = states, features=features, stateData=stateData, link = 'active')
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
    with open('v3/static/features.txt') as fp:
        features = fp.read().replace( '\r', '' ).split( '\n' )
    return features
    
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
