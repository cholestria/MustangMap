"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import State, StateData, HerdArea, AreaData

from model import connect_to_db, db
from server import app

from datetime import datetime
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

    for row in data:
        row = [element if len(element) > 0 else None for element in row]
        state_data = StateData(year=row[0],
                                state_id=row[1],
                                horse_adoptions=row[2],
                                burro_adoptions=row[3],
                                horse_removals=row[4],
                                burro_removals=row[5],)
        db.session.add(state_data)
    db.session.commit()

def load_herd_areas():
    """Load herd area info from herd_names.csv"""

    HerdArea.query.delete()  # deletes rows before adding so that data is not duplicated

    #reads the csv and inserts the data in the table
    csvfile = open('csvs/herd_names.csv')
    data = csv.reader(csvfile)
    next(data, None)  #skip the header row

    for row in data:
        row = [element if len(element) > 0 else None for element in row]
        herds = HerdArea(herd_id=row[0],
                            state_id=row[2],
                            herd_name=row[1],
                            gis_data=row[3],)

        db.session.add(herds)
    db.session.commit()

def load_herd_area_data():
    """Load per year herd area data from herd_data_by_year.csv"""

    AreaData.query.delete()  # deletes rows before adding so that data is not duplicated

    for year in range(2009, 2010):
        csvfile = open("csvs/"+str(year)+".csv")
        data = csv.reader(csvfile)
        next(data, None)  #skip the header row

        for row in data:
            row = [element if len(element) > 0 else None for element in row]
            if row[10] is not None:
                last_gather = datetime.strptime(row[10], '%B %Y')
            herd_info = AreaData(herd_id=row[1],
                                year=year,
                                ha_blm_acres=row[2],
                                ha_other_acres=row[3],
                                horse_population=row[7],
                                burro_population=row[9],
                                last_gather=last_gather)

            db.session.add(herd_info)
        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_states()
    load_state_data()
    load_herd_areas()
    load_herd_area_data()

