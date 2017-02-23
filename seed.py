"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import State, StateMapNames, StateData, HerdArea, HAData, HMAData, User, Facebook, Pictures

from model import connect_to_db, db
from server import app

from datetime import datetime
import csv

def delete_tables():
    """runs first to delete tables before insertion"""
    Pictures.query.delete()
    Facebook.query.delete()
    User.query.delete()
    HMAData.query.delete()
    HAData.query.delete()
    HerdArea.query.delete()
    StateData.query.delete()
    StateMapNames.query.delete()
    State.query.delete()

def load_states():
    """Load state info from sates_table.csv"""

    #reads the csv and inserts the data in the table
    csvfile = open('csvs/states_table.csv')
    data = csv.reader(csvfile)
    next(data, None)  # skip the headers

    for row in data:
        row = [element if len(element) > 0 else None for element in row]
        state = State(state_id=row[0],
                        name=row[1],
                        latitude=row[2],
                        longitude=row[3],
                        zoom=row[4])

        db.session.add(state)
    db.session.commit()

def load_maps():
    """Load state info from maps_table.csv"""

    #reads the csv and inserts the data in the table
    csvfile = open('csvs/maps_table.csv')
    data = csv.reader(csvfile)
    next(data, None)  # skip the headers

    for row in data:
        row = [element if len(element) > 0 else None for element in row]
        maps = StateMapNames(state_id=row[0],
                            map_name=row[1])

        db.session.add(maps)
    db.session.commit()

def load_state_data():
    """Load state data from state_data.csv"""

    # StateData.query.delete()  # deletes rows before adding so that data is not duplicated

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

    # HerdArea.query.delete()  # deletes rows before adding so that data is not duplicated

    #reads the csv and inserts the data in the table
    csvfile = open('csvs/herd_names.csv')
    data = csv.reader(csvfile)
    next(data, None)  #skip the header row

    for row in data:
        row = [element if len(element) > 0 else None for element in row]
        herds = HerdArea(herd_id=row[0],
                            state_id=row[2],
                            herd_name=row[1].title(),
                            gis_data=row[3],)

        db.session.add(herds)
    db.session.commit()

def load_herd_area_data():
    """Load per year herd area data from herd_data_by_year.csv"""

    # AreaData.query.delete()  # deletes rows before adding so that data is not duplicated

    #loops through all csv files and imports them
    for year in range(2005, 2017):
        csvfile = open("csvs/"+str(year)+".csv")
        data = csv.reader(csvfile)
        next(data, None)  #skip the header row


        for row in data:
            try:

                row = [element if len(element) > 0 else None for element in row]
                if row[15] is not None:
                    row[15] = datetime.strptime(row[15], '%B %Y')
                if row[14] is not None:
                    row[14] = datetime.strptime(row[14], '%B %Y')
                if row[16] is not None:
                    row[16] = datetime.strptime(row[16], '%Y')
                herd_info = HAData(herd_id=row[1],
                                    year=year,
                                    ha_blm_acres=row[2],
                                    ha_other_acres=row[3],
                                    horse_population=row[8],
                                    burro_population=row[12],
                                    last_gather=row[15])
                hma_info = HMAData(herd_id=row[1],
                                    year=year,
                                    hma_blm_acres=row[4],
                                    hma_other_acres=row[5],
                                    horse_aml_low=row[6],
                                    horse_aml_high=row[7],
                                    burro_aml_low=row[10],
                                    burro_aml_high=row[11],
                                    recent_count=row[14],
                                    most_recent_aml=row[16]
                                    )
                db.session.add(herd_info)
                db.session.add(hma_info)
            except Exception as detail:
                print "failed to insert" + str(row) + str(detail)
        db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    #deletes tables before seeding to avoid duplication
    delete_tables()

    # Import different types of data
    load_states()
    load_maps()
    load_state_data()
    load_herd_areas()
    load_herd_area_data()

