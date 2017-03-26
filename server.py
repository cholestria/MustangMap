"""Primary server file for Mustang Map."""
import os
import json
import bcrypt
import uuid
# from SQLAlchemy import SQLAlchemy

from jinja2 import StrictUndefined

from flask import Flask, url_for, request, send_from_directory, abort
from flask import render_template, redirect, flash, session
from flask_restful import reqparse, abort, Api, Resource
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

from model import connect_to_db, db, State, StateMapNames, StateData, HerdArea
from model import HAData, HMAData, User, Facebook, Pictures
from calculations import all_state_list, all_years_state_comparison
from mustangapi import PopByYearAPI, HerdAreaDataAPI, StateDataAPI, TotalDataAPI

class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'ABC')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'postgresql:///mustangs')
    CSRF_ENABLED = True
    UPLOAD_FOLDER =           os.getenv('UPLOAD_FOLDER',      'uploads/')

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_APP_NAME        = "AppName"                # Used by email templates


def setup_api(app):
    api = Api(app)

    api.add_resource(TotalDataAPI, '/totaldata')
    api.add_resource(StateDataAPI, '/statedata/<state_id>')
    api.add_resource(HerdAreaDataAPI, '/hachartdata/<herd_id>')
    api.add_resource(PopByYearAPI, '/popbyyear')

def create_app():
    """ Flask application factory """

    # Setup Flask app and app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Normally, if you use an undefined variable in Jinja2, it fails silently.
    # This is horrible. Fix this so that, instead, it raises an error.
    app.jinja_env.undefined = StrictUndefined

    # Initialize Flask extensions
    db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy
    mail = Mail(app)                                # Initialize Flask-Mail

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
    user_manager = UserManager(db_adapter, app)     # Initialize Flask-User


    @app.route('/')
    def homepage():
        """Homepage"""

        return render_template("splash.html")


    def creates_states_list():
        """Creates states list"""

        states_list = all_state_list()
        for state in states_list:
            state["file_names"] = [url_for("static", filename="geodata/"+each) for each in state["file_names"]]

        return states_list


    @app.route('/map')
    def newhomepage():
        """Homepage"""

        states_list = creates_states_list()
        states_dict = json.dumps(states_list)

        return render_template("homepage.html",
                               secret_key=os.environ['GOOGLE_MAPS_KEY'],
                               states=states_list,
                               states_dict=states_dict)


    @app.route('/login', methods=["GET"])
    def login():
        """Login Page"""

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

        abort(401)
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
        states_list = creates_states_list()

        return render_template("herdsearch.html",
                               herds=herds,
                               states=states_list)

    @app.route('/about')
    def about():
        """About Page """

        return render_template("about.html")

    return app


def run_app():
    app = create_app()
    connect_to_db(app)
    setup_api(app)
    app.run()

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True
    # app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # # Use the DebugToolbar
    # # DebugToolbarExtension(app)

    # app.run(port=5000, host='0.0.0.0')
    run_app()