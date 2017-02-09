"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class State(db.Model):
    """State list"""

    __tablename__ = "states"

    state_id = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self):
        """Prints state object information"""

        return "<State %s: %s>" % (self.state_id, self.name)


class StateData(db.Model):
    """Per State Data"""

    __tablename__ = "state_data"

    year = db.Column(db.Integer, nullable=False)
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
                "horse_adoptions": self.horse_adoptions
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

        return "<\nHerdArea %s -- id: %s in %s>" % (self.herd_name.title(), self.herd_id, self.state_id)


class HAData(db.Model):
    """Herd Area data per year"""

    __tablename__ = "ha_data_by_year"

    ha_by_year = db.Column(db.Integer, autoincrement=True, primary_key=True)
    herd_id = db.Column(db.Text,
        db.ForeignKey('herd_areas.herd_id'),
        nullable=False)
    year = db.Column(db.Integer)
    ha_blm_acres = db.Column(db.Integer, nullable=True)
    ha_other_acres = db.Column(db.Integer, nullable=True)
    horse_population = db.Column(db.Integer, nullable=True)
    burro_population = db.Column(db.Integer, nullable=True)
    last_gather = db.Column(db.DateTime, nullable=True)
    __table_args__ = (db.UniqueConstraint('year', 'herd_id'),
    )

    has = db.relationship('HerdArea', backref=db.backref('ha_data_by_year'))

    def __repr__(self):
        """Prints herd area data"""
        return "<\nHerdAreaData %s -- %s" % (self.herd_id, self.name)

class HMAData(db.Model):
    """Herd Management Area data per year"""

    __tablename__ = "hma_data_by_year"

    hma_yr_id = db.Column(db.Integer,
        db.ForeignKey('ha_data_by_year.ha_by_year'),
        primary_key=True,
        nullable=False)
    hma_blm_acres = db.Column(db.Integer, nullable=True)
    hma_other_acres = db.Column(db.Integer, nullable=True)
    horse_aml_low = db.Column(db.Integer, nullable=True)
    horse_aml_high = db.Column(db.Integer, nullable=True)
    burro_aml_low = db.Column(db.Integer, nullable=True)
    burro_aml_high = db.Column(db.Integer, nullable=True)
    recent_count = db.Column(db.DateTime, nullable=True)
    most_recent_aml = db.Column(db.DateTime, nullable=True)


    hmas = db.relationship('HAData', backref=db.backref('hma_data_by_year'))

    def __repr__(self):
        """Prints herd area data"""
        return "<\nHMAData %s -- %s" % (self.herd_id, self.name)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mustangs'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
