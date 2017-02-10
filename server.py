"""Mustang Data."""
import os

from jinja2 import StrictUndefined

from flask import Flask, jsonify
from flask import render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, State, StateData, HerdArea, HAData


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

def states_dictionary():
    """Makes States Dictionary"""

    states = [each for each in StateData.query.all()]
    states_dict = {}

    for i in states:
        if i.state_id not in states_dict:
            states_dict[(i.state_id)] = [i.year]
        else:
            states_dict[i.state_id].append(i.year)
    return states_dict

def state_by_year_info(st):
    """returns info by state per year"""

    all_years = [each for each in StateData.query.filter(StateData.state_id==st).all()]
    state_dict = {}

    for i in all_years:
        if i.year not in state_dict:
            state_dict[(i.year)] = [i.horse_adoptions, i.burro_adoptions, i.horse_removals, i.burro_removals]

    return state_dict



@app.route('/statedata/<st>')
def chart_per_state(st):
    """Chart Per State"""

    return jsonify(state_by_year_info(st))

@app.route('/chart/<st>')
def basic_chart(st):
    """Chart example"""

    return render_template("chart.html",
                            st=st)

@app.route('/')
def homepage():
    """Homepage"""

    states_dict = states_dictionary()

    return render_template("googlemapshomepage.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            states=states_dict)

@app.route('/data/<st>/<yr>')
def state_data_per_year(st, yr): #id must be combo of (year, state)
    """Mustang Data Per year"""

    state_data_per_year = StateData.query.get((int(yr), st))
    #example: StateData.query.get((2000,"CA"))


    return jsonify(state_data_per_year.dictionary_representation())



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
