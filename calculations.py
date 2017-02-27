from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea, HAData, HMAData
from flask import url_for

def all_state_list():
    """Makes States List"""

    states = State.query.all()
    states_list = []

    for i in states:
        state_dict = i.dictionary_representation()
        map_objects = StateMapNames.query.filter(StateMapNames.state_id==i.state_id).all()
        file_names = [each.map_name for each in map_objects]
        state_dict["file_names"] = file_names
        states_list.append(state_dict)

    return states_list


def state_map_dict(st):
    """Makes States Dictionary with map information"""

    state = State.query.filter(State.state_id==st).options(db.joinedload('maps')).first()
    state_dict = state.dictionary_representation()

    state_dict["map_names"] = [url_for("static", filename=each.map_name) for each in state.maps]

    return state_dict


def all_herds_list():
    """Makes Herd Areas List"""

    return [each.dictionary_representation() for each in HerdArea.query.all()]


def name_to_id_dictionary():
    """Makes Name to Id Dictionary"""

    states = StateData.query.options(db.joinedload('state')).all()
    states_dict = {}

    for i in states:
        states_dict[(i.state.name)] = [i.state_id]

    return states_dict


def id_to_name(st):
    """Returns a State Name Given a State ID"""

    states = State.query.filter_by(state_id=st).all()

    for i in states:
        return i.name


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

def ha_data_for_ha_chart(herd_id):
    """Returns the HA dictionary with additonal json information"""

    a_herd = HAData.query.filter(HAData.herd_id==herd_id).options(db.joinedload('herd_areas')).all()
    herd_name = a_herd[0].herd_areas.herd_name
    ha_pop_dict = {}
    footnote_dict = {}

    for i in a_herd:
        horse_population = i.horse_population
        burro_population = i.burro_population
        blm_acreage = i.ha_blm_acres
        other_acreage = i.ha_other_acres
        if i.horse_population is None:
            horse_population = 0
            footnote_dict[i.year] = "no horse population data reported for this year"
        if i.burro_population is None:
            burro_population = 0
            if i.year not in footnote_dict:
                footnote_dict[i.year] = "no burro population data reported for this year"
            else:
                footnote_dict[i.year].append("no burro population data reported for this year")
        if i.year not in ha_pop_dict:
            ha_pop_dict[(i.year)] = [horse_population, burro_population, blm_acreage, other_acreage]

    master_ha_dict = {"Name": herd_name,
        "Footnotes": footnote_dict,
        "PopData": ha_pop_dict,
        }

    return master_ha_dict

def state_by_year_info(st):
    """Returns per year removal and adoption info for a state"""

    all_years = StateData.query.filter(StateData.state_id==st).options(db.joinedload('state')).all()

    state_dict = {}
    footnote_dict = {}

    for i in all_years:
        horse_removals = i.horse_removals

        if i.horse_removals is None:
            horse_removals = 0
            footnote_dict[(i.year)] = "no horse removal data was reported"

        if i.year not in state_dict:
            state_dict[(i.year)] = [i.horse_adoptions, i.burro_adoptions, horse_removals, i.burro_removals]

    return state_dict


def state_pop_dict(st):
    """Returns dictionary of state population and acreage sums from herd data"""
    all_herds = ha_data_by_state(st)
    pop_dict = {}

    def make_horse_pop_sum(year):
        horse_pop = []
        for herd in all_herds:
            try:
                horse_pop.append(all_herds[str(herd)][year]['horse_population'])
            except:
                pass
        return sum(horse_pop)

    def make_burro_pop_sum(year):
        burro_pop = []
        for herd in all_herds:
            try:
                burro_pop.append(all_herds[str(herd)][year]['burro_population'])
            except:
                pass
        return sum(burro_pop)

    def make_blm_acreage_sum(year):
        blm_acres = []
        for herd in all_herds:
            try:
                blm_acres.append(all_herds[str(herd)][year]['ha_blm_acres'])
            except:
                pass
        return sum(blm_acres)

    def make_other_acreage_sum(year):
        other_acres = []
        for herd in all_herds:
            try:
                other_acres.append(all_herds[str(herd)][year]['ha_other_acres'])
            except:
                pass
        return sum(other_acres)

    for year in range(2005, 2017):
        if year not in pop_dict:
            pop_dict[year] = [make_horse_pop_sum(year), make_burro_pop_sum(year), make_blm_acreage_sum(year), make_other_acreage_sum(year)]

    return pop_dict


def master_state_dict(st):
    """creates a master dictionary that contains all state information"""
    all_years = StateData.query.filter(StateData.state_id==st).options(db.joinedload('state')).all()
    state_name = all_years[0].state.name

    pop_dict = state_pop_dict(st)
    state_dict = state_by_year_info(st)
    footnote_dict = {}  #emtpy for now
    map_dict = state_map_dict(st)

    master_state_dict = {"Name": state_name,
                "Footnotes": footnote_dict,
                "StateData": state_dict,
                "PopData": pop_dict,
                "MapDict": map_dict,
                }

    return master_state_dict


def total_horse_adoptions_per_year(yr):
    """Returns a total of horse adoptions across all states for year"""

    return db.session.query(db.func.sum(StateData.horse_adoptions)).filter(StateData.year==yr).one()[0]

def total_burro_adoptions_per_year(yr):
    """Returns a total of burro adoptions across all states for year"""

    return db.session.query(db.func.sum(StateData.burro_adoptions)).filter(StateData.year==yr).one()[0]

def total_horse_removals_per_year(yr):
    """Returns a total of horse removals across all states for year"""

    return db.session.query(db.func.sum(StateData.horse_removals)).filter(StateData.year==yr).one()[0]


def total_burro_removals_per_year(yr):
    """Returns a total of burro removals across all states for year"""

    return db.session.query(db.func.sum(StateData.burro_removals)).filter(StateData.year==yr).one()[0]


def total_horse_population_per_year(yr):
    """Returns a total of horse populations across all states for a year"""

    return db.session.query(db.func.sum(HAData.horse_population)).filter(HAData.year==yr).one()[0]


def total_burro_population_per_year(yr):
    """Returns a total of horse populations across all states for a year"""

    return db.session.query(db.func.sum(HAData.burro_population)).filter(HAData.year==yr).one()[0]

def total_blm_acres_per_year(yr):
    """Returns a total of horse populations across all states for a year"""

    return db.session.query(db.func.sum(HAData.ha_blm_acres)).filter(HAData.year==yr).one()[0]

def total_other_acres_per_year(yr):
    """Returns a total of horse populations across all states for a year"""

    return db.session.query(db.func.sum(HAData.ha_other_acres)).filter(HAData.year==yr).one()[0]


def all_states_pop_data():
    """Returns a dictionary of nationwide adoptions and removals"""

    all_data = HAData.query.options(db.joinedload('herd_areas')).all()
    pop_dict = {}

    for i in all_data:
        if i.year not in pop_dict:
            pop_dict[i.year] = [total_horse_population_per_year(i.year), total_burro_population_per_year(i.year), total_blm_acres_per_year(i.year), total_other_acres_per_year(i.year)]


def nationwide_pop_ar_totals():
    """Returns a dictionary of nationwide adoptions and removals"""

    all_data = StateData.query.options(db.joinedload('state')).all()
    all_pop_data = HAData.query.options(db.joinedload('herd_areas')).all()
    pop_dict = {}
    state_dict = {}
    footnote_dict = {}

    for i in all_data:
        horse_removals = i.horse_removals
        burro_removals = i.burro_removals
        if i.horse_removals is None:
            horse_removals = 0
            footnote_dict[(i.year)] = "no horse removal data was reported for this year"
        if i.burro_removals is None:
            burro_removals = 0
            footnote_dict[(i.year)] = "no burro removal data was reported for this year"

        if i.year not in state_dict:
            state_dict[i.year] = [total_horse_adoptions_per_year(i.year), total_burro_adoptions_per_year(i.year), total_horse_removals_per_year(i.year), total_burro_removals_per_year(i.year)]

    for i in all_pop_data:
        if i.year not in pop_dict:
            pop_dict[i.year] = [total_horse_population_per_year(i.year), total_burro_population_per_year(i.year), total_blm_acres_per_year(i.year), total_other_acres_per_year(i.year)]

    master_dict = {"Name": "Nationwide",
                    "Footnotes": footnote_dict,
                    "StateData": state_dict,
                    "PopData": pop_dict,
                    }

    return master_dict


def all_herds_dictionary():
    all_herds = HerdArea.query.options(db.joinedload('state')).all()
    herd_dict = {}

    for herd in all_herds:
        if herd.state.name not in herd_dict:
            herd_dict[herd.state.name] = [i.herd_name]
        else:
            herd_dict[herd.state.name].append(herd.herd_name)

    return herd_dict


def all_years_state_comparison():
    """Returns all population data for all years and all states"""

    pop_data = HAData.query.options(db.joinedload('herd_areas')).all()
    all_dict = {}

    for i in pop_data:
        if i.year in all_dict:
            year = all_dict[i.year]
        else:
            year = {}
        if i.herd_areas.state_id in year:
            state = year[i.herd_areas.state_id]
        else:
            state = {"horse": 0, "burro": 0}
        if i.horse_population is not None:
            state["horse"] = state["horse"] + i.horse_population
        if i.burro_population is not None:
            state["burro"] = state["burro"] + i.burro_population
        year[i.herd_areas.state_id] = state
        all_dict[i.year] = year

    return all_dict
