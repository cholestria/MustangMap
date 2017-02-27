"""Mustang Data."""
import os
import json
import bcrypt

from jinja2 import StrictUndefined

from flask import Flask, jsonify, url_for, request, send_from_directory
from flask import render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea, HAData, HMAData, User, Facebook, Pictures
from calculations import all_state_list, ha_data_by_state, state_by_year_info, ha_data_for_ha_chart, name_to_id_dictionary, master_state_dict
from calculations import nationwide_pop_ar_totals, all_years_state_comparison, all_herds_dictionary

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Homepage"""

    states_dict = all_state_list()
    # name_to_id = name_to_id_dictionary()
    all_pop_dict = all_years_state_comparison()
    all_pop = json.dumps(all_pop_dict)

    return render_template("googlemapshomepage.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            states=states_dict,
                            name_to_id=name_to_id,
                            all_pop=all_pop)

@app.route('/map')
def newhomepage():
    """Homepage"""

    states_list = all_state_list()
    for state in states_list:
        state["file_names"] = [url_for("static", filename=each) for each in state["file_names"]]
    # name_to_id = name_to_id_dictionary()
    all_pop_dict = all_years_state_comparison()
    all_pop = json.dumps(all_pop_dict)
    states_dict = json.dumps(states_list)

    return render_template("homepage.html",
                            secret_key=os.environ['GOOGLE_MAPS_KEY'],
                            states=states_list,
                            # name_to_id=name_to_id,
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
        return redirect("/map")
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
        return redirect("/map")  # or user's page?


@app.route('/logout')
def logout():
    """Logs user out"""

    del session['user_id']

    return login()


@app.route('/pictures')
def pictures():

    return render_template("pictures.html")


@app.route('/upload', methods=['GET'])
def upload():

    return render_template('upload.html')


def allowed_file(filename):
    return'.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        name = request.form.get("name")
        herd_id = request.form.get("herd_id")
        picture_credit = request.form.get("pc")
        user_id = session['user_id']

        new_picture = Pictures(name=name,
                                herd_id=herd_id,
                                picture_credit=picture_credit,
                                user_id=user_id,
                                filename=filename)
        db.session.add(new_picture)
        db.session.commit()
        return redirect("/pictures/" + filename)


@app.route('/pictures/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/hachartdata/<herd_id>')
def herd_area_data(herd_id):
    """Population per year for each herd area"""

    return jsonify(ha_data_for_ha_chart(herd_id))


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


@app.route('/statedata/<st>')
def chart_per_state(st):
    """Adoption and Removal Chart Per State"""

    return jsonify(master_state_dict(st))


@app.route('/popbyyear/<yr>')
def populations_by_year(yr):
    """Populations of All States by Year"""

    return jsonify(all_years_state_comparison())


@app.route('/totaldata')
def total_data():
    """Adoption and Removal Chart totaled"""

    return jsonify(nationwide_pop_ar_totals())



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
