"""Mustang Data."""
import os

from jinja2 import StrictUndefined

from flask import Flask, jsonify
from flask import render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, State, StateData, HerdArea, HAData


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

    states = StateData.query.all()

    return render_template("googlemapshomepage.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            states=states)






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
