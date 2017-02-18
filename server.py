"""Mustang Data."""
import os
import json

from jinja2 import StrictUndefined

from flask import Flask, jsonify
from flask import render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea, HAData, HMAData
from calculations import states_dictionary, ha_data_by_state, state_by_year_info, ha_data_for_ha_chart, name_to_id_dictionary, master_state_dict
from calculations import nationwide_pop_ar_totals, all_years_state_comparison, all_herds_dictionary

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
    name_to_id = name_to_id_dictionary()
    all_pop_dict = all_years_state_comparison()
    all_pop = json.dumps(all_pop_dict)

    return render_template("googlemapshomepage.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            states=states_dict,
                            name_to_id=name_to_id,
                            all_pop=all_pop)

@app.route('/map')
def newhomepage():
    """Homepage"""

    states_dict = states_dictionary()
    name_to_id = name_to_id_dictionary()
    all_pop_dict = all_years_state_comparison()
    all_pop = json.dumps(all_pop_dict)

    return render_template("homepage.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            states=states_dict,
                            name_to_id=name_to_id,
                            all_pop=all_pop)


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

    return jsonify(master_state_dict(st))


@app.route('/popbyyear/<yr>')
def populations_by_year(yr):
    """Populations of All States by Year"""

    return jsonify(all_years_state_comparison())


@app.route('/totaldata')
def total_data():
    """Adoption and Removal Chart totaled"""

    return jsonify(nationwide_pop_ar_totals())


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

    states_dict = states_dictionary()

    state_maps = StateMapNames.query.filter(StateMapNames.state_id==state_id).all()
    state_info = State.query.filter(State.state_id==state_id).one()

    return render_template("statemap.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            state_id=state_id,
                            state_info=state_info,
                            state_maps=state_maps,
                            states=states_dict)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
