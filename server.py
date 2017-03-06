"""Mustang Data."""
import os
import json
import bcrypt
import uuid

from jinja2 import StrictUndefined

from flask import Flask, jsonify, url_for, request, send_from_directory
from flask import render_template, redirect, flash, session
from flask_restful import reqparse, abort, Api, Resource
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea
from model import HAData, HMAData, User, Facebook, Pictures
from calculations import all_state_list, all_years_state_comparison
from mustangapi import PopByYearAPI, HerdAreaDataAPI, StateDataAPI, TotalDataAPI

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

api = Api(app)


@app.route('/')
def homepage():
    """Homepage"""

    return render_template("splash.html")


@app.route('/map')
def newhomepage():
    """Homepage"""

    states_list = all_state_list()
    for state in states_list:
        state["file_names"] = [url_for("static", filename=each) for each in state["file_names"]]
    all_pop_dict = all_years_state_comparison()
    all_pop = json.dumps(all_pop_dict)
    states_dict = json.dumps(states_list)

    return render_template("homepage.html",
                           secret_key=os.environ['GOOGLE_MAPS_KEY'],
                           states=states_list,
                           all_pop=all_pop,
                           states_dict=states_dict)


@app.route('/login', methods=["GET"])
def login():
    """Login Page"""

    states_list = all_state_list()
    for state in states_list:
        state["file_names"] = [url_for("static", filename=each) for each in state["file_names"]]

    return render_template("login.html")


@app.route('/login', methods=["POST"])
def handle_login():
    """Sends user information to the database"""
    email = request.form.get("email")
    password = request.form.get("password")
    hypothetical_user = User.query.filter_by(email=email).first()
    if hypothetical_user is None:
        flash("That email hasn't been registered. Please register.")
        return login()
    if bcrypt.hashpw(password, hypothetical_user.password) == hypothetical_user.password:
        session['user_id'] = hypothetical_user.user_id
        flash("You're now logged in.")
        return redirect("/upload")
    else:
        flash("Wrong password")
        return login()


@app.route('/register', methods=["POST"])
def create_user():
    """Process registration form"""

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if User.query.filter_by(email=email).first() is not None:
        flash("Email is already registered. Please sign in.")
        return login()
    else:
        new_user = User(name=name, email=email, password=bcrypt.hashpw(password, bcrypt.gensalt()))
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.user_id

        flash("Thanks for signing up. You're now logged in.")
        return redirect("/map")  # or user's page?


@app.route('/logout')
def logout():
    """Logs user out"""

    del session['user_id']

    return login()


@app.route('/picturepage/<herd_id>')
def pictures():
    """Shows all Pictures for a Herd Area"""

    return render_template("pictures.html")


@app.route('/upload', methods=['GET'])
def upload():
    """Returns the Upload Page"""

    herds = [each.dictionary_representation() for each in HerdArea.query.all()]

    return render_template('upload.html',
                            herds=herds)


def allowed_file(filename):
    return'.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    """Uploads an Image to the Database"""
    #check if the post request includes the file part
    if 'file' not in request.files:
        flash('No file part')
        return upload()
    file = request.files['file']
    #if user does not select file or submit a part without filename
    if file.filename == '':
        flash('No file selected')
        return upload()
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename, file_extension = os.path.splitext(filename)
        new_filename = str(uuid.uuid4())
        total_filename = new_filename + file_extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], total_filename))

        name = request.form.get("name")
        herd_id = request.form.get("herd_id")
        picture_credit = request.form.get("pc")
        user_id = session['user_id']

        new_picture = Pictures(name=name,
                               herd_id=herd_id,
                               picture_credit=picture_credit,
                               user_id=user_id,
                               filename=total_filename)
        db.session.add(new_picture)
        db.session.commit()
        return redirect("/pictures/" + total_filename)


@app.route('/pictures/<filename>')
def uploaded_file(filename):
    """Image Path"""
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/herdsearch')
def herd_search():
    """Herd List and Search page"""

    herds = [each.dictionary_representation() for each in HerdArea.query.all()]
    states_list = all_state_list()
    for state in states_list:
        state["file_names"] = [url_for("static", filename=each) for each in state["file_names"]]

    return render_template("herdsearch.html",
                           herds=herds,
                           states=states_list)


@app.route('/about')
def about():
    """About Page """

    return render_template("about.html")


api.add_resource(TotalDataAPI, '/totaldata')
api.add_resource(StateDataAPI, '/statedata/<state_id>')
api.add_resource(HerdAreaDataAPI, '/hachartdata/<herd_id>')
api.add_resource(PopByYearAPI, '/popbyyear')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
