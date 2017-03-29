"""Models and database functions for cars db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Part 1: Compose ORM


# look at relationships - read the data modeling lecture about many to many

class Show(db.Model):
    """Runway show details."""

    __tablename__ = "shows"

    show_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    season_id = db.Column(db.Integer,
                          db.ForeignKey('seasons.season_id'))
    brand_id = db.Column(db.Integer,
                         db.ForeignKey('brands.brand_id'))
    designer_id = db.Column(db.Integer,
                            db.ForeignKey('designers.designer_id')
                            nullable=True)
    # unicode text ere and for allstrings
    review_text = db.Column(db.String(255),
                            nullable=True)
    # add a location (location id) AND a datetime (datetime id) 
    # two new tables with relationships


    # Define relationship to season
    seasons = db.relationship('Season')

    # def __repr__(self):
    #     return "<Brand brand_id=%s name=%s founded=%s hq=%s>" % (
    #         self.brand_id,
    #         self.name,
    #         self.founded,
    #         self.headquarters)


class Season(db.Model):
    """Season info."""

    __tablename__ = "seasons"

    season_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    year = db.Column(db.Integer)
    season = db.Column(db.String(2))

    # Define relationship to Show
    shows = db.relationship('Show')

    # def __repr__(self):
    #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
    #         self.model_id,
    #         self.brand_id,
    #         self.name,
    #         self.year)


class Show_Color(db.Model):
    """Show specific color info."""

    __tablename__ = "show_colors"

    show_colors_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey('shows.show_id'))
    color_id = db.Column(db.Integer,
                         db.ForeignKey('colors.color_id'))

    # Define relationship to Show
    shows = db.relationship('Show')
    colors = db.relationship('Color')

    # def __repr__(self):
    #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
    #         self.model_id,
    #         self.brand_id,
    #         self.name,
    #         self.year)


class Color(db.Model):
    """Show specific color info."""

    __tablename__ = "colors"

    color_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    color_name = db.Column(db.Unicode)
    # do a sep RGB table if needed but dont worry about it!
    # NEED TO DEFINE HEX RANGES HERE - not anymore!
    # LIKE THREE ROWS FOR R (INT 265) G (INT 265) & B (INT 265)

    # Define relationship to Show
    show_colors = db.relationship('Show_Color')

    # def __repr__(self):
    #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
    #         self.model_id,
    #         self.brand_id,
    #         self.name,
    #         self.year)


class Image(db.Model):
    """Show image info."""

    __tablename__ = "images"

    image_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey('shows.show_id'))
    image_url = db.Column(db.Unicode(1024))

    # Define relationship to Show_Color
    show_id = db.relationship('Show')

    # def __repr__(self):
    #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
    #         self.model_id,
    #         self.brand_id,
    #         self.name,
    #         self.year)


class Brand(db.Model):
    """Show brand info."""

    __tablename__ = "brands"

    brand_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    brand_name = db.Column(db.String(50))

    # Define relationship to Show
    shows = db.relationship('Show')

    # def __repr__(self):
    #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
    #         self.model_id,
    #         self.brand_id,
    #         self.name,
    #         self.year)


class Designer(db.Model):
    """Show designer name info."""
    # add a show_desigenr column with s_d_id and show_id and designer_id

    __tablename__ = "designers"

    designer_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    designer_name = db.Column(db.String(50))

    # Define relationship to Show/Brand
    shows = db.relationship('Show')
    brands = db.relationship('Brand')

    # def __repr__(self):
    #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
    #         self.model_id,
    #         self.brand_id,
    #         self.name,
    #         self.year)


class Keyword_Show(db.Model):
    """Show specific color info."""

    __tablename__ = "keyword_shows"

    keyword_id = db.Column(db.Integer,
                           db.ForeignKey('keywords.keyword_id'))
    show_id = db.Column(db.Integer,
                        db.ForeignKey('shows.show_id'))
    keyword_show_id = db.Column(db.Integer,
                                primary_key=True,
                                db.ForeignKey('colors.color_id'))

    # Define relationship to Show
    keywords = db.relationship('Keyword')
    shows = db.relationship('Show')
    colors = db.relationship('Color')
    # def __repr__(self):
    #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
    #         self.model_id,
    #         self.brand_id,
    #         self.name,
    #         self.year)


class Keyword(db.Model):
    """Show specific color info. elim k_s table put sho-id here"""

    __tablename__ = "keywords"

    keyword_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    word = db.Column(db.String(50),
                     db.ForeignKey('shows.show_id'))

    # Define relationship to Show
    keyword_show = db.relationship('Keyword_Show')

    # def __repr__(self):
    #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
    #         self.model_id,
    #         self.brand_id,
    #         self.name,
    #         self.year)


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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///cars'
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
