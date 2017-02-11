"""Models and database functions for MustangMap project."""

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

    def dictionary_representation(self):

        return {"state_id": self.state_id,
                "name": self.name,
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
        return "\n<HerdAreaData %s -- year: %s, horse pop: %s, burro pop: %s" % (self.herd_id, self.year, self.horse_population, self.burro_population )

    def dictionary_representation(self):

        return {"herd_id": self.herd_id,
                "year": self.year,
                "ha_blm_acres": self.ha_blm_acres,
                "ha_other_acres": self.ha_other_acres,
                "horse_population": self.horse_population,
                "last_gather": self.burro_population,
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

    herd_area = db.relationship('HerdArea', backref=db.backref('hma_data_by_year'))

    def __repr__(self):
        """Prints herd area data"""
        return "\n<HMAData %s -- %s" % (self.herd_id, self.name)

    def dictionary_representation(self):

        return {"herd_id": self.herd_id,
                "year": self.year,
                "hma_blm_acres": self.hma_blm_acres,
                "hma_other_acres": self.hma_other_acres,
                }

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
    db.create_all()
    print "Connected to DB."
