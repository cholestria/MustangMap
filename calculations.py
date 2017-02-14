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
    herd_dict = {}

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
        if year not in herd_dict:
            herd_dict[year] = []


    #creates a master dictionary that contains all information
    master_state_dict = {"StateName": state_name,
                "Footnotes": footnote_dict,
                "StateData": state_dict,
                "PopData": pop_dict,
                }

    return master_state_dict


