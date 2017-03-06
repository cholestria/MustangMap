import unittest

from flask import Flask
from calculations import ha_data_by_state, all_state_list, all_years_state_comparison, ha_data_for_ha_chart, state_adopt_removal_data
from model import connect_to_db, db

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"

connect_to_db(app, 'postgresql:///mustangs')

def run(case):
    suite = unittest.TestLoader().loadTestsFromTestCase(case)
    unittest.TextTestRunner(verbosity=2).run(suite)


class TestAssert(unittest.TestCase):
    def test_assert(self):
        """Tests if the ha_data_by_state function works by checking the horse population
        in Palomino Buttes for 2016"""
        palomino_buttes = ha_data_by_state("OR")["OR0006"][2016]['horse_population']
        self.assertEquals(palomino_buttes, 131)

run(TestAssert)


class TestAssert2(unittest.TestCase):
    def test_assert2(self):
        """Tests if the ha_data_for_ha_chart function works by checking the burro population
        in Centennial for 2006"""
        centennial = ha_data_for_ha_chart("CA0654")["PopData"][2006][1]
        self.assertEquals(centennial, 125)

run(TestAssert)


class TestAssert3(unittest.TestCase):
    def test_assert3(self):
        """Tests if the state_adopt_removal_data function works by checking the
        horse removals in Nevada for 2009"""
        nevada2009 = state_adopt_removal_data("NV")[2009][2]
        self.assertEquals(nevada2009, 2158)

run(TestAssert)

class TestAssert4(unittest.TestCase):
    def test_assert3(self):
        """Tests if the state_pop_dict function works by checking the
        total acreage in Wyoming for 2012"""
        wyoming = state_pop_dict("WY")[2012][3]
        self.assertEquals(wyoming, 10344424)

run(TestAssert)


class TestAssert5(unittest.TestCase):
    def test_assert3(self):
        """Tests if the nationwide_population_totals function works by checking the
        total horses for 2008"""
        nationwide = nationwide_population_totals()[2008][0]
        self.assertEquals(nationwide, 23815)

run(TestAssert)



