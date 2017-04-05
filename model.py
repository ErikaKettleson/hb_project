"""Models and database functions for showme db."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################

class Show(db.Model):
    """Runway show details."""

    __tablename__ = "shows"

    show_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    season = db.Column(db.String(6))
    year = db.Column(db.Integer)
    brand_id = db.Column(db.Integer,
                         db.ForeignKey('brands.brand_id'))

    # Define relationship to brands
    brands = db.relationship('Brand')

    def __repr__(self):
        return "<Show show_id=%s season=%s brand_id=%s year=%s>" % (
            self.show_id,
            self.season,
            self.brand_id,
            self.year)


class Show_Color(db.Model):
    """Association table connecting specific color info to shows."""

    __tablename__ = "show_colors"

    show_colors_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey('shows.show_id'))
    color_id = db.Column(db.Integer,
                         db.ForeignKey('colors.color_id'))

    # Define relationship to Show & Color tables
    shows = db.relationship('Show')
    colors = db.relationship('Color')

    def __repr__(self):
        return "<Show_Color show_color_id=%s show_id=%s color_id=%s" % (
            self.show_color_id,
            self.show_id,
            self.color_id)


class Color(db.Model):
    """Show specific color name/hex info."""

    __tablename__ = "colors"

    color_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    color_name = db.Column(db.Unicode)
    color_hex = db.Column(db.Unicode)

    def __repr__(self):
        return "<Color color_id=%s color_name=%s>" % (
            self.color_id,
            self.color_name)


class Brand(db.Model):
    """Show brand info."""

    __tablename__ = "brands"

    brand_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    brand_name = db.Column(db.String(50))

    # Define relationship to Show
    shows = db.relationship('Show')

    def __repr__(self):
        return "<Model brand_name=%s brand_id=%s>" % (
            self.brand_name,
            self.brand_id)

##############################################################################
# Helper functions


def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///showme'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
