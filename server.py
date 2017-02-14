"""Mustang Data."""
import os

from jinja2 import StrictUndefined

from flask import Flask, jsonify
from flask import render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea, HAData, HMAData
from calculations import population_density


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

def ha_data_by_state(st):
    """Returns a dictionary of population and acreage per HA within a state"""

    herds = HAData.query.options(db.joinedload('herd_areas')).all()
    dictionary = {}

    for i in herds:
        if i.herd_areas.state_id==st:
            if i.herd_id not in dictionary:
                dictionary[i.herd_id] = {i.year: i.dictionary_representation()}
            else:
                dictionary[i.herd_id][i.year] = i.dictionary_representation()
    return dictionary

def state_by_year_info(st):
    """Returns per year removal and adoption info for a state"""

    all_years = StateData.query.filter(StateData.state_id==st).options(db.joinedload('state')).all()
    state_name = all_years[0].state.name
    all_herds = ha_data_by_state(st)

    state_dict = {}
    footnote_dict = {}
    pop_dict = {}

    for i in all_years:
        horse_removals = i.horse_removals

        if i.horse_removals is None:
            horse_removals = 0
            footnote_dict[(i.year)] = "no horse removal data was reported"

        if i.year not in state_dict:
            state_dict[(i.year)] = [i.horse_adoptions, i.burro_adoptions, horse_removals, i.burro_removals]

    def make_horse_pop_sum(year):
        horse_pop = []
        for herd in all_herds:
            horse_pop.append(all_herds[str(herd)][year]['horse_population'])
        return sum(horse_pop)

    def make_burro_pop_sum(year):
        burro_pop = []
        for herd in all_herds:
            burro_pop.append(all_herds[str(herd)][year]['burro_population'])
        return sum(burro_pop)

    def make_blm_acreage_sum(year):
        blm_acres = []
        for herd in all_herds:
            blm_acres.append(all_herds[str(herd)][year]['ha_blm_acres'])
        return sum(blm_acres)

    def make_other_acreage_sum(year):
        other_acres = []
        for herd in all_herds:
            other_acres.append(all_herds[str(herd)][year]['ha_other_acres'])
        return sum(other_acres)

    for year in range(2015, 2017):
        if year not in pop_dict:
            pop_dict[year] = [make_horse_pop_sum(year), make_burro_pop_sum(year), make_blm_acreage_sum(year), make_other_acreage_sum(year)]

    #creates a master dictionary that contains all information
    master_state_dict = {"StateName": state_name,
                "Footnotes": footnote_dict,
                "StateData": state_dict,
                "PopData": pop_dict,
                }

    return master_state_dict

@app.route('/')
def homepage():
    """Homepage"""

    states_dict = states_dictionary()

    return render_template("googlemapshomepage.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            states=states_dict)


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
