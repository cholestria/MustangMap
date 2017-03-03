from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea, HAData, HMAData, User, Pictures
from flask import url_for
import random


def all_state_list():
    """Makes States List"""

    states = State.query.all()
    states_list = []

    for i in states:
        state_dict = i.dictionary_representation()
        map_objects = StateMapNames.query.filter(StateMapNames.state_id == i.state_id).all()
        file_names = [each.map_name for each in map_objects]
        state_dict["file_names"] = file_names
        states_list.append(state_dict)

    return states_list


def state_map_dict(st):
    """Makes States Dictionary with map information"""

    #used in master_state_dict(st)

    state = State.query.filter(State.state_id == st).options(db.joinedload('maps')).first()
    map_dict = state.dictionary_representation()

    map_dict["map_names"] = [url_for("static", filename=each.map_name) for each in state.maps]

    return map_dict


def ha_data_by_state(st):
    """Returns a dictionary of population and acreage per HA within a state"""

    #used in state_pop_dict(st)

    herds = HAData.query.options(db.joinedload('herd_areas')).all()
    dictionary = {}

    for i in herds:
        if i.herd_areas.state_id == st:
            if i.herd_id not in dictionary:
                dictionary[i.herd_id] = {i.year: i.dictionary_representation()}
            else:
                dictionary[i.herd_id][i.year] = i.dictionary_representation()
    return dictionary


def find_pictures_by_herd_id(herd_id):
    "Returns pictures of Mustangs from a particular herd area"

    #used in herd_area_data

    picture_info = Pictures.query.filter(Pictures.herd_id == herd_id).options(db.joinedload('users')).all()
    length = len(picture_info)
    picture_dict = {}

    if length == 0:
        picture_dict["none"] = {"none": "none"}
    else:
        if length > 1:
            index = random.randint(0, (length-1))
        else:
            index = 0
        selected_picture = picture_info[index]
        picture_dict = {}

        picture_dict[selected_picture.filename] = {"horse": selected_picture.name, "credit": selected_picture.picture_credit, "user": selected_picture.users.name}

    return picture_dict


def ha_data_for_ha_chart(herd_id):
    """Returns the HA dictionary with additonal json information"""

    #used in hachartdata jsonify

    a_herd = HAData.query.filter(HAData.herd_id == herd_id).options(db.joinedload('herd_areas')).all()
    herd_name = a_herd[0].herd_areas.herd_name
    ha_pop_dict = {}
    footnote_dict = {}
    pictures = find_pictures_by_herd_id(herd_id)

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
                      "Pictures": pictures,
                      }

    return master_ha_dict


def state_adopt_removal_data(st):
    """Returns per year removal and adoption info for a state"""

    #used in master_state_dict(st)

    all_years = StateData.query.filter(StateData.state_id == st).options(db.joinedload('state')).all()

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

    #used in master_state_dict(st)

    all_herds = ha_data_by_state(st)
    pop_dict = {}
    years = [each[1].keys() for each in all_herds.items()][0]

    for year in years:
        if year not in pop_dict:
            horse_pop = 0
            burro_pop = 0
            blm_acreage = 0
            total_acreage = 0
            for herd_data in all_herds.values():
                try:
                    year_data = herd_data[year]
                    horse_pop += year_data['horse_population']
                    burro_pop += year_data['burro_population']
                    blm_acreage += year_data['ha_blm_acres']
                    total_acreage += year_data['ha_other_acres']
                except:
                    pass
            pop_dict[year] = [horse_pop, burro_pop, blm_acreage, total_acreage]
    return pop_dict


def master_state_dict(st):
    """Creates a master dictionary that contains all state information"""

    #returned as json for statedata/st

    all_years = StateData.query.filter(StateData.state_id == st).options(db.joinedload('state')).all()
    state_name = all_years[0].state.name

    pop_dict = state_pop_dict(st)
    adopt_dict = state_adopt_removal_data(st)
    footnote_dict = {}  #emtpy for now
    map_dict = state_map_dict(st)

    master_state_dict = {"Name": state_name,
                         "Footnotes": footnote_dict,
                         "AdoptData": adopt_dict,
                         "PopData": pop_dict,
                         "MapDict": map_dict,
                         }

    return master_state_dict


def nationwide_population_totals():
    """Returns nationwide population and acreage data for all years"""

    #used in the nationwide master dictionary

    pop_data = HAData.query.options(db.joinedload('herd_areas')).all()
    pop_dict = {}

    for i in pop_data:
        if i.year in pop_dict:
            year = pop_dict[i.year]
        else:
            year = [0, 0, 0, 0]
        if i.horse_population is not None:
            year[0] = year[0] + i.horse_population
        if i.burro_population is not None:
            year[1] = year[1] + i.burro_population
        if i.ha_blm_acres is not None:
            year[2] = year[2] + i.ha_blm_acres
        if i.ha_other_acres is not None:
            year[3] = year[3] + i.ha_other_acres

        pop_dict[i.year] = year

    return pop_dict


def nationwide_pop_ar_totals():
    """Returns a master dictionary of nationwide adoptions and removals and populations"""

    #used in /totaldata json

    all_data = StateData.query.options(db.joinedload('state')).all()
    adopt_dict = {}
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

        if i.year in adopt_dict:
            year = adopt_dict[i.year]
        else:
            year = [0, 0, 0, 0]
        if i.horse_adoptions is not None:
            year[0] = year[0] + i.horse_adoptions
        if i.burro_adoptions is not None:
            year[1] = year[1] + i.burro_adoptions
        if i.horse_removals is not None:
            year[2] = year[2] + i.horse_removals
        if i.burro_removals is not None:
            year[3] = year[3] + i.burro_removals

        adopt_dict[i.year] = year

    master_dict = {"Name": "Nationwide",
                   "Footnotes": footnote_dict,
                   "AdoptData": adopt_dict,
                   "PopData": nationwide_population_totals(),
                   }

    return master_dict


def all_years_state_comparison():
    """Returns all population data for all years and all states"""

    #used in the heat maps function

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
