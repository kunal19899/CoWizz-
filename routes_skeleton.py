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
    return render_template("index_skeleton.html", states = states, features = features, stateData='', link = '')


@app.route("/animate", methods=['POST'])
def animate():
    ################ complete animate function to parse input here ##############

    return 
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
    ################ Write your code here to load the required csv file and compute the total deaths and cases for states
    
    return
    #################################################################################################################
    
# api functions beyond this point

if __name__ == "__main__":
    app.run( debug=True)
