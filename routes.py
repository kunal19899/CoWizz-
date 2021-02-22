from flask import render_template, redirect, request, url_for, session, flash
import requests
from v3.forms import InputForm
from datetime import datetime, timedelta
from v3.article_search import ArticleSearch
from flask import Flask
from v3 import app
from v3 import static
from v3.map_test import map_test
import csv
from v3.feature_graph import main

@app.route("/")
def index():
    inputForm = InputForm()
    states = load_states()
    features = load_features()
    return render_template("index.html", form = inputForm, states = states, features = features, link = '')


@app.route("/animate", methods=['POST'])
def animate():
    ################ complete animate function to parse input here ##############
    stateList=[]
    inputForm = InputForm()
    states = load_states()
    features = load_features()
    if request.method == "POST":
        ipt = request.form
        for item in ipt:
            if item != 'feature1':
                stateList.append(ipt[item])
            else: break
        link = main(stateList, ipt['feature1'], ipt['feature2'])
    return render_template('index.html', form = inputForm, states = states, features=features, link = link)
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


# api functions beyond this point

if __name__ == "__main__":
    app.run( debug=True)
