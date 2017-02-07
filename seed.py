"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import State, StateData, HerdArea, AreaData

from model import connect_to_db, db
from server import app

# from datetime import datetime
import csv


def load_states():
    """Load state info from sates.csv"""

    State.query.delete()  # deletes rows before adding so that data is not duplicated

    #reads the csv and inserts the data in the table
    csvfile = open('csvs/states_table.csv')
    data = csv.reader(csvfile)
    next(data, None)  # skip the headers

    for each in data:
        state = State(state_id=each[0],
                        state_name=each[1])

        db.session.add(state)
    db.session.commit()

def load_state_data():
    """Load state data from state_data.csv"""

    StateData.query.delete()  # deletes rows before adding so that data is not duplicated

    #reads the csv and inserts the data in the table
    csvfile = open('csvs/state_data.csv')
    data = csv.reader(csvfile)
    next(data, None)  #skip the header row

    for each in data:
        state_data = StateData(year=each[0],
                                state_id=each[1],
                                horse_adoptions=each[2],
                                burro_adoptions=each[3],
                                horse_removals=each[4],
                                burro_removals=each[5],)
        db.session.add(state_data)
    db.session.commit()

def load_herd_areas():
    """Load herd area info from herd_names.csv"""

    HerdArea.query.delete()  # deletes rows before adding so that data is not duplicated

    #reads the csv and inserts the data in the table
    csvfile = open('csvs/herd_names.csv')
    data = csv.reader(csvfile)
    next(data, None)  #skip the header row

    for each in data:
        herds = HerdAreas(herd_id=each[0],
                            state_id=each[2],
                            name=each[1],
                            gis=each[3],)

        db.session.add(herds)
    db.session.commit()

# def load_herd_area_data():
#     """Load per year herd area data from herd_data_by_year.csv"""

#     AreaData.query.delete()  # deletes rows before adding so that data is not duplicated

#     for year in range(2005, 2010):
#         csvfile = open(str(year)+".csv")
#         data = csv.reader(csvfile)
#         next(data, None)  #skip the header row

#         for each in data:
#             herd_info = HerdAreas(herd_id=each[1],
#                                 year=year,
#                                 ha_blm_acres=each[2],
#                                 ha_other_acres=each[3],
#                                 horse_population=each[7],
#                                 burro_population=each[9],
#                                 last_gather=each[10])

#             db.session.add(herd_info)
#         db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_states()
    load_state_data()
    load_herd_areas()

