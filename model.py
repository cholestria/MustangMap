"""Models and database functions for MustangMap project."""

from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

db = SQLAlchemy()

class State(db.Model):
    """State list"""

    __tablename__ = "states"

    state_id = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    zoom = db.Column(db.Integer, nullable=True)


    def __repr__(self):
        """Prints state object information"""

        return "<State %s: %s>" % (self.state_id, self.name)

    def dictionary_representation(self):

        return {"state_id": self.state_id,
                "name": self.name,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "zoom": self.zoom,
                }

class StateMapNames(db.Model):
    """Map names"""

    ___tablename__ = "maps"

    state_id = db.Column(db.String(3),
                db.ForeignKey('states.state_id'),
                primary_key=True,
                nullable=True)
    map_name = db.Column(db.Text,
                        primary_key=True,
                        nullable=True)

    state =  db.relationship('State', backref=db.backref('maps'))

    def __repr__(self):
        """Prints map object information"""

        return "<Map %s: %s.>" % (self.state_id, self.map_name)

    def dictionary_representation(self):

        return {"state_id": self.state_id,
                "map_name": self.map_name,
                }

class StateData(db.Model):
    """Per State Data"""

    __tablename__ = "state_data"

    year = db.Column(db.Integer, nullable=False, autoincrement=False)
    state_id = db.Column(db.String(3),
        db.ForeignKey('states.state_id'),
        nullable=False)
    horse_adoptions = db.Column(db.Integer, nullable=True, default=None)
    burro_adoptions = db.Column(db.Integer, nullable=True, default=None)
    horse_removals = db.Column(db.Integer, nullable=True, default=None)
    burro_removals = db.Column(db.Integer, nullable=True, default=None)
    __table_args__ = (db.PrimaryKeyConstraint('year', 'state_id', name="state_per_year"),
        )

    state = db.relationship('State', backref=db.backref('state_data'))

    def __repr__(self):
        """Prints state data information"""

        return "<\nStateData %s %s -- horses adopted: %s burros adopted: %s\n horses removed: %s burros removed: %s>" % (self.year, self.state_id, self.horse_adoptions, self.burro_adoptions, self.horse_removals, self.burro_removals)

    def dictionary_representation(self):

        return {"year": self.year,
                "state_id": self.state_id,
                "horse_adoptions": self.horse_adoptions,
                "burro_adoptions": self.burro_adoptions,
                "horse_removals": self.horse_removals,
                "burro_removals": self.burro_removals,
                }

class HerdArea(db.Model):
    """Herd Area basic information"""

    __tablename__ = "herd_areas"

    herd_id = db.Column(db.Text, primary_key=True)
    herd_name = db.Column(db.Text, nullable=False)
    state_id = db.Column(db.String(3),
        db.ForeignKey('states.state_id'),
        nullable=False)
    gis_data = db.Column(db.Text, nullable=True)

    state = db.relationship('State', backref=db.backref('herd_areas'))

    def __repr__(self):
        """Prints herd area information"""

        return "\n<HerdArea %s -- id: %s in %s>" % (self.herd_name.title(), self.herd_id, self.state_id)

    def dictionary_representation(self):

        return {"herd_id": self.herd_id,
                "herd_name": self.herd_name,
                "state_id": self.state_id,
                }

class HAData(db.Model):
    """Herd Area data per year"""

    __tablename__ = "ha_data_by_year"

    herd_id = db.Column(db.Text,
        db.ForeignKey('herd_areas.herd_id'),
        nullable=False)
    year = db.Column(db.Integer, nullable=False, autoincrement=False)
    ha_blm_acres = db.Column(db.Integer, nullable=True)
    ha_other_acres = db.Column(db.Integer, nullable=True)
    horse_population = db.Column(db.Integer, nullable=True)
    burro_population = db.Column(db.Integer, nullable=True)
    last_gather = db.Column(db.DateTime, nullable=True)
    __table_args__ = (db.PrimaryKeyConstraint('herd_id', 'year'),
    )

    herd_areas = db.relationship('HerdArea', backref=db.backref('ha_data_by_year'))

    def __repr__(self):
        """Prints herd area data"""
        return "\n<HerdAreaData %s -- year: %s, horse pop: %s, burro pop: %s>" % (self.herd_id, self.year, self.horse_population, self.burro_population )

    def dictionary_representation(self):
        if self.ha_other_acres is None:
            ha_other_acres = 0
        else:
            ha_other_acres = self.ha_other_acres
        if self.ha_blm_acres is None:
            ha_blm_acres = 0
        else:
            ha_blm_acres = self.ha_blm_acres
        if self.horse_population is None:
            horse_population = 0
        else:
            horse_population = self.horse_population
        if self.burro_population is None:
            burro_population = 0
        else:
            burro_population = self.burro_population

        return {"herd_id": self.herd_id,
                "year": self.year,
                "ha_blm_acres": ha_blm_acres,
                "ha_other_acres": ha_other_acres,
                "horse_population": horse_population,
                "burro_population": burro_population,
                "last_gather": self.last_gather,
                }

class HMAData(db.Model):
    """Herd Management Area data per year"""

    __tablename__ = "hma_data_by_year"

    herd_id = db.Column(db.Text,
        db.ForeignKey('herd_areas.herd_id'),
        nullable=False)
    year = db.Column(db.Integer, nullable=False, autoincrement=False)

    hma_blm_acres = db.Column(db.Integer, nullable=True)
    hma_other_acres = db.Column(db.Integer, nullable=True)
    horse_aml_low = db.Column(db.Integer, nullable=True)
    horse_aml_high = db.Column(db.Integer, nullable=True)
    burro_aml_low = db.Column(db.Integer, nullable=True)
    burro_aml_high = db.Column(db.Integer, nullable=True)
    recent_count = db.Column(db.DateTime, nullable=True)
    most_recent_aml = db.Column(db.DateTime, nullable=True)

    __table_args__ = (db.PrimaryKeyConstraint('herd_id', 'year'),
    )

    herd_areas = db.relationship('HerdArea', backref=db.backref('hma_data_by_year'))

    def __repr__(self):
        """Prints herd area data"""
        return "\n<HMAData %s for %s -- horse high aml: %s burrow high aml: %s>" % (self.herd_id, self.year, _by, self.horse_aml_high, self.burro_aml_high )

    def dictionary_representation(self):

        return {"herd_id": self.herd_id,
                "year": self.year,
                "hma_blm_acres": self.hma_blm_acres,
                "hma_other_acres": self.hma_other_acres,
                }

class User(db.Model, UserMixin):
    """User of MustangMap website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    #User information
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False, server_default='')

    #user email information
    email = db.Column(db.Text, nullable=True)
    confirmed_at = db.Column(db.DateTime())

    #user_information
    name = db.Column(db.Text, nullable=False)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')

    def __repr__(self):
        """Prints user information"""

        return "\n<User: %s with email: %s>" % (self.name, self.email)


class Facebook(db.Model):
    """Facebook information for Users"""

    __tablename__ = "facebook"

    user_id = db.Column(db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False)

    facebook_id = db.Column(db.Text, primary_key=True, nullable=True)

    users = db.relationship('User', backref=db.backref('facebook'))

    def __repr__(self):
        """Prints user facebook information"""

        return "\n<User: %s with facebook userID: %s>" % (self.user_id, self.facebook_id)


class Pictures(db.Model):
    """Pictures Uploaded By Users"""

    __tablename__ = "pictures"

    user_id = db.Column(db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False)
    name = db.Column(db.Text, nullable=True)
    picture_credit = db.Column(db.Text, nullable=True)
    filename = db.Column(db.Text, primary_key=True, nullable=False)
    herd_id = db.Column(db.Text,
        db.ForeignKey('herd_areas.herd_id'),
        nullable=False)

    users = db.relationship('User', backref=db.backref('pictures'))
    herd_areas = db.relationship('HerdArea', backref=db.backref('pictures'))

    def __repr__(self):
        """Prints picture information"""

        return "\n<Filename: %s with with herd ID: %s>" % (self.filename, self.herd_id)


##############################################################################
# Helper functions

def connect_to_db(app, uri='postgresql:///mustangs'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
