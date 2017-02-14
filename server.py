"""Mustang Data."""
import os

from jinja2 import StrictUndefined

from flask import Flask, jsonify
from flask import render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea, HAData, HMAData
from calculations import states_dictionary, ha_data_by_state, state_by_year_info, ha_data_for_ha_chart


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():
    """Homepage"""

    states_dict = states_dictionary()

    return render_template("googlemapshomepage.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            states=states_dict)

@app.route('/hachart/<herd_id>')
def herd_area_chart(herd_id):
    """Population per year for each herd area"""

    return render_template("hachart.html",
                            herd_id=herd_id)


@app.route('/hachartdata/<herd_id>')
def herd_area_data(herd_id):
    """Population per year for each herd area"""

    return jsonify(ha_data_for_ha_chart(herd_id))


@app.route('/statedata/<st>')
def chart_per_state(st):
    """Adoption and Removal Chart Per State"""

    return jsonify(state_by_year_info(st))


@app.route('/chart/<st>')
def basic_chart(st):
    """Chart of Adoptions and removals over time"""

    return render_template("chart.html",
                            st=st)


@app.route('/popchart/<st>')
def pop_chart_by_state(st):

    return render_template('popchart.html',
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
