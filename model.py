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
    season = db.Column(db.String(5))
    year = db.Column(db.Integer)
    brand_id = db.Column(db.Integer,
                         db.ForeignKey('brands.brand_id'))
    designer_id = db.Column(db.Integer,
                            db.ForeignKey('designers.designer_id')
                            nullable=True)

    # Define relationship to season
    brands = db.relationship('Brand')
    designers = db.relationship('Designer')

    def __repr__(self):
        return "<Show show_id=%s season=%s brand_id=%s year=%s>" % (
            self.show_id,
            self.season,
            self.brand_id,
            self.year)


class Show_Color(db.Model):
    """Show specific color info."""

    __tablename__ = "show_colors"

    show_colors_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey('shows.show_id'))
    color_id_1 = db.Column(db.Integer,
                           db.ForeignKey('colors.color_id_1'))
    color_id_2 = db.Column(db.Integer,
                           db.ForeignKey('colors.color_id_2'))
    color_id_3 = db.Column(db.Integer,
                           db.ForeignKey('colors.color_id_3'))
    color_id_4 = db.Column(db.Integer,
                           db.ForeignKey('colors.color_id_4'))
    color_id_5 = db.Column(db.Integer,
                           db.ForeignKey('colors.color_id_5'))
    color_id_6 = db.Column(db.Integer,
                           db.ForeignKey('colors.color_id_6'))

    # Define relationship to Show
    shows = db.relationship('Show')
    colors = db.relationship('Color')

    def __repr__(self):
        return "<Show_Color show_color_id=%s show_id=%s color_id_1=%s" % (
            self.show_color_id,
            self.show_id,
            self.color_id_1)


class Color(db.Model):
    """Show specific color info."""

    __tablename__ = "colors"

    color_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    color_name = db.Column(db.Unicode)

    # Define relationship to Show
    show_colors = db.relationship('Show_Color')

    def __repr__(self):
        return "<Color color_id=%s color_name=%s>" % (
            self.color_id,
            self.color_name)


# class Image(db.Model):
#     """Show image info."""

#     __tablename__ = "images"

#     image_id = db.Column(db.Integer,
#                          autoincrement=True,
#                          primary_key=True)
#     show_id = db.Column(db.Integer,
#                         db.ForeignKey('shows.show_id'))
#     image_url = db.Column(db.Unicode(1024))

#     # Define relationship to Show_Color
#     show_id = db.relationship('Show')

#     def __repr__(self):
#         return "<Image image_id=%s show_id=%s image_url=%s>" % (
#             self.image_id,
#             self.show_id,
#             self.image_url)


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


# class Designer(db.Model):
#     """Show designer name info."""
#     # add a show_desigenr column with s_d_id and show_id and designer_id

#     __tablename__ = "designers"

#     designer_id = db.Column(db.Integer,
#                             autoincrement=True,
#                             primary_key=True)
#     designer_name = db.Column(db.String(50))

#     # Define relationship to Show/Brand
#     shows = db.relationship('Show')
#     brands = db.relationship('Brand')

#     # def __repr__(self):
#     #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
#     #         self.model_id,
#     #         self.brand_id,
#     #         self.name,
#     #         self.year)


# class Keyword_Show(db.Model):
#     """Show specific color info."""

#     __tablename__ = "keyword_shows"

#     keyword_show_id = db.Column(db.Integer,
#                                 primary_key=True,
#                                 db.ForeignKey('keywords.keyword_id'))
#     keyword_id = db.Column(db.Integer,
#                            db.ForeignKey('keywords.keyword_id'))
#     review_json = db.Column(db.JSONB)
#     show_id = db.Column(db.Integer,
#                         db.ForeignKey('shows.show_id'))

#     # Define relationship to Show
#     keywords = db.relationship('Keyword')
#     shows = db.relationship('Show')
#     colors = db.relationship('Color')
#     # def __repr__(self):
#     #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
#     #         self.model_id,
#     #         self.brand_id,
#     #         self.name,
#     #         self.year)


# class Keyword(db.Model):
#     """Show specific keyword info. elim k_s table put sho-id here"""

#     __tablename__ = "keywords"

#     keyword_id = db.Column(db.Integer,
#                            autoincrement=True,
#                            primary_key=True)
#     word = db.Column(db.String(50),
#                      db.ForeignKey('shows.show_id'))

#     # Define relationship to Show
#     keyword_show = db.relationship('Keyword_Show')

#     # def __repr__(self):
#     #     return "<Model model_id=%s brand_id=%s name=%s year=%s>" % (
#     #         self.model_id,
#     #         self.brand_id,
#     #         self.name,
#     #         self.year)


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
