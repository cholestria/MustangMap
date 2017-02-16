from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea, HAData, HMAData

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

def name_to_id_dictionary():
    """Makes Name to Id Dictionary"""

    states = StateData.query.options(db.joinedload('state')).all()
    states_dict = {}

    for i in states:
            states_dict[(i.state.name)] = [i.state_id]

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

    for year in range(2015, 2017):
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

    master_state_dict = {"Name": state_name,
                "Footnotes": footnote_dict,
                "StateData": state_dict,
                "PopData": pop_dict,
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

def all_states_ar_data():
    """Returns a dictionary of nationwide adoptions and removals"""

    all_data = StateData.query.options(db.joinedload('state')).all()

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

    master_dict = {"Name": "Nationwide",
                "Footnotes": footnote_dict,
                "StateData": state_dict,
                "PopData": "Empty"
                }

    return master_dict
