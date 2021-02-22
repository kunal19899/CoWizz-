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
    return render_template("index.html", form = inputForm, states = states)


@app.route("/animate", methods=['POST'])
def animate():
    ################ complete animate function to parse input here ##############

    return
    #############################################################################


def load_states():
    states_names = []
    with open('v3/static/states.csv') as states:
        states_map = csv.reader(states, delimiter=',')
        for state, abbr in states_map:
            if state != "State":
                states_names.append(state)
    return states_names


# api functions beyond this point

if __name__ == "__main__":
    app.run( debug=True)
