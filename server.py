from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify, Response
from flask_debugtoolbar import DebugToolbarExtension
from model import Show, Show_Color, Brand, Color, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
import flask_restless
import json

from sqlalchemy.sql import func

from sqlalchemy import create_engine, Column, Integer, String, Date, Float


app = Flask(__name__)
# app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///showme'
db = flask_sqlalchemy.SQLAlchemy(app)

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
show_blueprint = manager.create_api(Show, methods=['GET'])
brand_blueprint = manager.create_api(Brand, methods=['GET'])
color_blueprint = manager.create_api(Color, methods=['GET'])
show_color_blueprint = manager.create_api(Show_Color, methods=['GET'])

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    """Homepage."""
    shows = Show.query.all()
    show_colors = Show_Color.query.all()
    colors = Color.query.all()
    brands = Brand.query.all()

    return render_template("bleep.html",
                           shows=shows,
                           show_colors=show_colors,
                           colors=colors,
                           brands=brands)


@app.route('/_get_brands')
def get_brands_json():
    brands = {}
    for brand in Brand.query.all():
        brands[brand.brand_id] = {
            'brand_name': brand.brand_name,
        }

    return jsonify(brands)


@app.route('/_get_shows')
def get_shows_json():
    shows = {}
    for show in Show.query.all():
        shows[show.show_id] = {
            'show_id': show.show_id,
            'show_season': show.season,
            'show_year': show.year,
            'brand_name': show.brands.brand_name,
        }

    return jsonify(shows)


@app.route('/_get_colors')
def get_colors_json():
    colors = {}
    for color in Color.query.all():
        colors[color.color_id] = {
            'color_id': color.color_id,
            'color': color.color_name,
            'color_hex': color.color_hex,
        }

    return jsonify(colors)


@app.route('/_get_show_colors')
def get_show_colors_json():
    show_colors_json = {}
    for show_color in Show_Color.query.all():
        show_colors_json[show_color.show_colors_id] = {
            'show_color': show_color.colors.color_id,
            'brand_name': show_color.shows.brands.brand_name,
            'color_id': show_color.color_id,
            'color_name': show_color.colors.color_name,
        }

    return jsonify(show_colors_json)


@app.route('/_get_color_by_brand')
def get_colors_by_brand_json():
    brands = Brand.query.all()
    brand_by_colors = {brand.brand_name: [] for brand in brands}
    for brand in brands:
        shows = Show.query.filter_by(
            brand_id=brand.brand_id,
        ).all()
        for show in shows:
            show_colors = Show_Color.query.filter_by(
                show_id=show.show_id,
            ).all()
            for color in show_colors:
                color_objects = Color.query.filter_by(
                    color_id=color.color_id,
                ).all()
                for color_object in color_objects:
                    brand_by_colors[brand.brand_name].append(
                        color_object.color_name
                    )

    return jsonify(brand_by_colors)

# <Show_Color show_colors_id=1 show_id=1 color_id=2


@app.route('/colorsovertime')
def colors_over_time():

    return render_template("colorsovertime.html")

# @app.route('/streams')
# def stream_me():

#     return render_template("streamgraph.html")

# what i want: {'x=season': epoch time, 'y=count': color_count}
# each colo should have 2 dicts - count for fall,, count for spring
# a list of colors in each season, and their counts
# start off with year = Show.query.filter_by(year).all()
# then with the season = Show.query.filter_by(season).all()
# then with a list of the colors featured in season with hex value & count
# color_name, color_hex = db.engine.execute("SELECT color_name, color_hex FROM colors WHERE color_id='x'"),

    # final series empty list, append indv series to the series list up here
    # examine types of series - make sure they are the type you think


@app.route("/temp")
def temp():
    series = []

    color_data = db.engine.execute("SELECT color_id, shows.season, shows.year, COUNT(*) FROM show_colors JOIN shows ON show_colors.show_id=shows.show_id GROUP BY color_id, shows.season, shows.year")

    for l in color_data:
        color_id = l[0],
        # color_id:tuple
        # print color_id, type(color_id)
        season = l[1],
        # season:tuple
        # print season, type(season)
        year = l[2],
        # year: tuple
        # print year, type(year)
        color_count = l[3]
        # color_count: long - type of int
        # print color_count, type(color_count)

        # if year == 2017:
        if season[0] == 'spring':
            # print "season at 0 is spring"
            epoch_time = 1501545600
        elif season[0] == 'fall':
            # print "season at 0 is fall"
            epoch_time = 1485907200
        else: 
            print season, type(season)

        color_n = db.engine.execute("SELECT color_name FROM colors WHERE color_id=color_id")
        color_n1 = color_n.fetchone()
        color_name = color_n1.values()
        color_h = db.engine.execute("SELECT color_hex FROM colors WHERE color_id=color_id")
        color_h1 = color_h.fetchone()
        color_hex = color_h1.values()

        series.append([
            {'name': color_name,
             'data': [{'x': epoch_time, 'y': color_count}],
             'color': color_hex
             }
             ])

    # import ipdb; ipdb.set_trace()
    # print "series", series, type(series)
    return Response(json.dumps(series),  mimetype='application/json')
    # return jsonify(series)


@app.route('/stream')
def make_stream():
    # testing out streamgraph

    # JUST WRITE A SQLALCHEMY QUERY TO RETREIVE:
    """SELECT color_name, color_hex, count(color_name)
    FROM colors 
    JOIN show_colors ON color_id=show_colors.color_id
    WHERE show.year=2017, show.season=fall
    """

    years = [2017]
    seasons = ['fall', 'spring']
    color_counter = []
    import time
    print("AHHHHHHHHHHH!")
    start_time = time.time()
    for year in years:
        print("year", year)
        for season in seasons:
            print("season", season)
            # give me all shows for each season
            shows = Show.query.filter_by(season=season).all()
            for show_id in shows:
                print("show_id", show_id)
                # give me all colors for all shows in season
                show_colors = Show_Color.query.filter_by(show_id=Show.show_id).all()
                for color in show_colors:
                    print("color", color)
                    color_objects = Color.query.filter_by(color_id=color.color_id).all()
                    for color_object in color_objects:
                        color_counter.append(
                            (color_object.color_name, color_object.color_hex)
                        )

            counts = {color: color_counter.count(color) for color in color_counter}
            color_name_hex, color_count = counts.keys(), counts.values()
            color_by_name = []
            color_by_hex = []
            for n, h in color_name_hex:
                color_by_name.append(n)
                color_by_hex.append(h)

            for color in color_by_name:
                for hex_val in color_by_hex:
                    color_name = color
                    color_hex = hex_val

            if year == 2017:
                if season == 'spring':
                    epoch_time = 1501545600
                elif season == 'fall':
                    epoch_time = 1485907200

            series = [
                    {'name': color_name,
                     'data': [{'x': epoch_time, 'y': color_count}],
                     'color': color_hex
                     }
                     ]
    stop_time = time.time()
    print(stop_time-start_time)
    print jsonify(series)
    return jsonify(series)


@app.route('/pie')
def pie():

    brand_id = request.args.get('brand_id')
    season = request.args.get('season')
    year = request.args.get('year')

    if brand_id == 'All':
        brand_id = []
        for brand in Brand.query.all():
            brand_id.append(brand.brand_id)
    # import ipdb; ipdb.set_trace()
    color_counter = []

    for brand_id in brand_id:
        if season != 'All':
            if season == 'Fall':
                shows = Show.query.filter_by(season='fall', brand_id=brand_id).all()
            elif season == 'Spring':
                shows = Show.query.filter_by(season='spring', brand_id=brand_id).all()
        else:
            shows = Show.query.filter_by(brand_id=brand_id).all()
    # need a year if else statement here once older years seeded
        for show in shows:
            show_colors = Show_Color.query.filter_by(show_id=show.show_id).all()
            for color in show_colors:
                color_objects = Color.query.filter_by(color_id=color.color_id).all()
                for color_object in color_objects:
                    color_counter.append(
                        (color_object.color_name, color_object.color_hex)
                    )

        counts = {color: color_counter.count(color) for color in color_counter}
        color_name_hex, color_count = counts.keys(), counts.values()
        color_by_name = []
        color_by_hex = []
        for n, h in color_name_hex:
            color_by_name.append(n)
            color_by_hex.append(h)

        x = color_by_name
        data_color = color_count
        backgroundColor = color_by_hex
        hoverBackgroundColor = color_by_hex

        data = {
            'labels': x,
            'datasets': [{
                'data': data_color,
                'backgroundColor': backgroundColor,
                'hoverBackgroundColor': hoverBackgroundColor
            }]
        }

    return jsonify(data)

    # show_id route that returns show_id:[color_id[10]]
    # think about the fxn as connectiing many - one color/show/etc

# import ipdb; ipdb.set_trace()

# Query: show all colors, all season/years for 1 brand
# need show_id, color_id, color_hex, season, year, brand_id
# show.show_id
# show.show_colors.color_id
# show.show_colors.color_hex
# show.brands.brand_name

# Query: show all shows/all seasons/all colors
# need all show_id, year, season, brand_name, color_id, color_hex
# show_color.shows.brands.brand_name
# show_color.shows.show_id
# show_color.shows.season
# show_color.shows.year
# show_color.color_id
# show_color.colors.color_hex

# Query: show color over time
# need all color_id/hex & all show_id for all year/season
# color.color_id
# color.color_hex
# color.color_name
# color.show_colors.show_id
# color.show_colors.shows.season
# color.show_colors.shows.year




# @webapp.route('/api/<color_hex>')
# def api_by_season(color_hex):
#     events = Events.query.filter_by(event_type=event_type).all()
#     return jsonify(json_list=[event.serialize for event in events])


# @app.route('/', methods=['GET'])
# def register_form():
#     """Show form for user signup."""

#     return render_template("base.html")


# @app.route('/register', methods=['POST'])
# def register_process():
#     """Process registration."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]
#     age = int(request.form["age"])
#     zipcode = request.form["zipcode"]

#     new_user = User(email=email, password=password, age=age, zipcode=zipcode)

#     db.session.add(new_user)
#     db.session.commit()

#     flash("User %s added." % email)
#     return redirect("/")


# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""

#     return render_template("login_form.html")


# @app.route('/login', methods=['POST'])
# def login_process():
#     """Process login."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]

#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash("No such user")
#         return redirect("/login")

#     if user.password != password:
#         flash("Incorrect password")
#         return redirect("/login")

#     session["user_id"] = user.user_id

#     flash("Logged in")
#     return redirect("/users/%s" % user.user_id)


# @app.route('/logout')
# def logout():
#     """Log out."""

#     del session["user_id"]
#     flash("Logged Out.")
#     return redirect("/")


# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


# @app.route("/users/<int:user_id>")
# def user_detail(user_id):
#     """Show info about user."""

#     user = User.query.get(user_id)
#     return render_template("user.html", user=user)


# @app.route("/movies")
# def movie_list():
#     """Show list of movies."""

#     movies = Movie.query.order_by('title').all()
#     return render_template("movie_list.html", movies=movies)


# @app.route("/movies/<int:movie_id>", methods=['GET'])
# def movie_detail(movie_id):
#     """Show info about movie.

#     If a user is logged in, let them add/edit a rating.
#     """

#     movie = Movie.query.get(movie_id)

#     user_id = session.get("user_id")

#     if user_id:
#         user_rating = Rating.query.filter_by(
#             movie_id=movie_id, user_id=user_id).first()

#     else:
#         user_rating = None

#     # Get average rating of movie

#     rating_scores = [r.score for r in movie.ratings]
#     avg_rating = float(sum(rating_scores)) / len(rating_scores)

#     prediction = None

#     # Prediction code: only predict if the user hasn't rated it.

#     if (not user_rating) and user_id:
#         user = User.query.get(user_id)
#         if user:
#             prediction = user.predict_rating(movie)

#     # Either use the prediction or their real rating

#     if prediction:
#         # User hasn't scored; use our prediction if we made one
#         effective_rating = prediction

#     elif user_rating:
#         # User has already scored for real; use that
#         effective_rating = user_rating.score

#     else:
#         # User hasn't scored, and we couldn't get a prediction
#         effective_rating = None

#     # Get the eye's rating, either by predicting or using real rating

#     the_eye = (User.query.filter_by(email="the-eye@of-judgment.com")
#                          .one())
#     eye_rating = Rating.query.filter_by(
#         user_id=the_eye.user_id, movie_id=movie.movie_id).first()

#     if eye_rating is None:
#         eye_rating = the_eye.predict_rating(movie)

#     else:
#         eye_rating = eye_rating.score

#     if eye_rating and effective_rating:
#         difference = abs(eye_rating - effective_rating)

#     else:
#         # We couldn't get an eye rating, so we'll skip difference
#         difference = None

    # Depending on how different we are from the Eye, choose a
    # message

#     BERATEMENT_MESSAGES = [
#         "I suppose you don't have such bad taste after all.",
#         "I regret every decision that I've ever made that has " +
#             "brought me to listen to your opinion.",
#         "Words fail me, as your taste in movies has clearly " +
#             "failed you.",
#         "That movie is great. For a clown to watch. Idiot.",
#         "Words cannot express the awfulness of your taste."
#     ]

#     if difference is not None:
#         beratement = BERATEMENT_MESSAGES[int(difference)]

#     else:
#         beratement = None

#     return render_template(
#         "movie.html",
#         movie=movie,
#         user_rating=user_rating,
#         average=avg_rating,
#         prediction=prediction,
#         eye_rating=eye_rating,
#         difference=difference,
#         beratement=beratement
#         )


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def movie_detail_process(movie_id):
#     """Add/edit a rating."""

#     # Get form variables
#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("No user logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash("Rating updated.")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Rating added.")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
