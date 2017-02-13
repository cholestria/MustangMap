"""Mustang Data."""
import os

from jinja2 import StrictUndefined

from flask import Flask, jsonify
from flask import render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea, HAData, HMAData


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

def states_dictionary():
    """Makes States Dictionary"""

    states = StateData.query.options(db.joinedload('state')).all()
    states_dict = {}

    for i in states:
        if i.state_id not in states_dict:
            states_dict[(i.state_id)] = [i.state.name]
        else:
            states_dict[i.state_id].append(i.year)
    return states_dict

def state_by_year_info(st):
    """Returns per year removal and adoption info for a state"""

    all_years = StateData.query.filter(StateData.state_id==st).options(db.joinedload('state')).all()
    state_name = all_years[0].state.name
    state_dict = {}
    footnote_dict = {}

    for i in all_years:
        horse_removals = i.horse_removals

        if i.horse_removals is None:
            horse_removals = 0
            footnote_dict[(i.year)] = "no horse removal data was reported"

        if i.year not in state_dict:
            state_dict[(i.year)] = [i.horse_adoptions, i.burro_adoptions, horse_removals, i.burro_removals]

    #creates a master dictionary that contains all information
    master_state_dict = {"StateName": state_name,
                "Footnotes": footnote_dict,
                "StateData": state_dict,
                }

    return master_state_dict
    #make json return each year's data as a dictionary instead of list

@app.route('/')
def homepage():
    """Homepage"""

    states_dict = states_dictionary()

    return render_template("googlemapshomepage.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            states=states_dict)


@app.route('/statedata/<st>')
def chart_per_state(st):
    """Chart Per State"""

    return jsonify(state_by_year_info(st))


@app.route('/population/<st>')
def populations_by_state(st):
    """Returns JSON of state horse and burro population data"""



@app.route('/chart/<st>')
def basic_chart(st):
    """Chart example"""

    return render_template("chart.html",
                            st=st)


@app.route('/map/<state_id>')
def state_map(state_id):
    """State map"""

    state_maps = StateMapNames.query.filter(StateMapNames.state_id==state_id).all()
    state_info = State.query.filter(State.state_id==state_id).one()

    return render_template("statemap.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            state_id=state_id,
                            state_info=state_info,
                            state_maps=state_maps)

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
