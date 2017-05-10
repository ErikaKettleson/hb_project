from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify, Response
from model import Show, Show_Color, Brand, Color, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
import flask_restless
import json

from sqlalchemy.sql import func

from sqlalchemy import create_engine, Column, Integer, String, Date, Float, func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///showme'
db = flask_sqlalchemy.SQLAlchemy(app)

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
show_blueprint = manager.create_api(Show, methods=['GET'])
brand_blueprint = manager.create_api(Brand, methods=['GET'])
color_blueprint = manager.create_api(Color, methods=['GET'])
show_color_blueprint = manager.create_api(Show_Color, methods=['GET'])

# Required to use Flask sessions and the debug toolbar
app.secret_key = "XoC92aXfNMKLKR5"

# allows undefined jinja variables to raise an error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/brands')
def index():
    """shows the colors by brands page."""
    shows = Show.query.all()
    show_colors = Show_Color.query.all()
    colors = Color.query.all()
    brands = Brand.query.all()

    return render_template("brands.html",
                           shows=shows,
                           show_colors=show_colors,
                           colors=colors,
                           brands=brands)


@app.route('/bubbles')
def colors_over_time():
    # shows the colors over time page
    return render_template("bubble.html")


@app.route('/')
def about_showme():
    # shows the about page
    return render_template("about.html")


@app.route('/palettes')
def palette():
    # shows the color explorer page
    return render_template("palette.html")


@app.route('/_get_show_colors')
def get_show_colors_json():
    # json for the color explorer page chart
    years = [2012, 2013, 2014, 2015, 2016, 2017, 2018]
    data_d = {'datasets': []}
    sorted_rainbow_hex = {'#808080': 138, '#ADFF2F': 77, '#FFB6C1': 1, '#556B2F': 78, '#FF8C00': 107, '#9932CC': 19, '#8A2BE2': 21, '#BA55D3': 17, '#2F4F4F': 53, '#00008B': 30, '#DB7093': 5, '#0000FF': 28, '#DC143C': 3, '#DDA0DD': 11, '#4169E1': 33, '#DA70D6': 9, '#DCDCDC': 134, '#7B68EE': 23, '#AFEEEE': 49, '#E6E6FA': 26, '#800080': 16, '#FFF5EE': 114, '#6B8E23': 80, '#FF69B4': 6, '#000080': 32, '#228B22': 72, '#008B8B': 54, '#5F9EA0': 46, '#EE82EE': 12, '#D3D3D3': 135, '#FF00FF': 14, '#48D1CC': 56, '#FFFFFF': 132, '#F5DEB3': 97, '#00FA9A': 61, '#F08080': 124, '#808000': 86, '#FAEBD7': 103, '#A9A9A9': 137, '#7FFFD4': 59, '#C0C0C0': 136, '#7FFF00': 75, '#FFEBCD': 101, '#B0C4DE': 35, '#008080': 55, '#FFFACD': 88, '#FFD700': 91, '#000000': 140, '#008000': 73, '#8B4513': 113, '#FFF0F5': 4, '#FFFFF0': 83, '#6A5ACD': 24, '#FFFAFA': 123, '#4682B4': 40, '#FFEFD5': 100, '#EEE8AA': 89, '#00FF00': 71, '#FFDEAD': 102, '#CD853F': 109, '#ADD8E6': 44, '#E0FFFF': 48, '#F8F8FF': 27, '#D8BFD8': 10, '#BC8F8F': 125, '#FF6347': 120, '#FF0000': 127, '#00CED1': 52, '#A0522D': 115, '#FFC0CB': 2, '#9370DB': 22, '#CD5C5C': 126, '#FFF8DC': 92, '#800000': 131, '#B8860B': 94, '#FFA07A': 116, '#40E0D0': 58, '#FAFAD2': 82, '#DEB887': 105, '#F0FFFF': 47, '#2E8B57': 65, '#E9967A': 119, '#87CEEB': 42, '#D2B48C': 104, '#90EE90': 67, '#00FFFF': 51, '#8FBC8F': 69, '#7CFC00': 76, '#FFE4E1': 121, '#BDB76B': 87, '#F4A460': 111, '#F0FFF0': 66, '#9400D3': 18, '#3CB371': 64, '#F5FFFA': 62, '#20B2AA': 57, '#1E90FF': 38, '#708090': 37, '#F5F5DC': 81, '#66CDAA': 60, '#9ACD32': 79, '#C71585': 8, '#F5F5F5': 133, '#32CD32': 70, '#8B0000': 130, '#696969': 139, '#191970': 29, '#0000CD': 31, '#00BFFF': 43, '#483D8B': 25, '#6495ED': 34, '#FFA500': 99, '#00FF7F': 63, '#A52A2A': 128, '#FAF0E6': 108, '#778899': 36, '#FFE4B5': 98, '#B22222': 129, '#DAA520': 93, '#4B0082': 20, '#FFFAF0': 95, '#B0E0E6': 45, '#F0E68C': 90, '#FFFF00': 85, '#006400': 74, '#FFE4C4': 106, '#FDF5E6': 96, '#8B008B': 15, '#FF7F50': 117, '#FFFFE0': 84, '#FA8072': 122, '#FFDAB9': 110, '#D2691E': 112, '#FF1493': 7, '#98FB98': 68, '#F0F8FF': 39, '#87CEFA': 41, '#FF4500': 118}

    color_object = Color.query.all()
    for color in color_object:
        color_id = color.color_id
        color_name = color.color_name
        color_hex = color.color_hex
        rainbow_connection = sorted_rainbow_hex[color_hex.upper()]

        for year in years:
            radius = db.session.query(Show_Color).join(Show).filter_by(year=year).filter(Show_Color.color_id == color_id).count()
            radius = radius*.5

            my_dataset = {
                 'label': color_name,
                 'data': [{'x': rainbow_connection, 'y': year, 'r': radius}],
                 'backgroundColor': color_hex,
                 'hoverBackgroundColor': color_hex,
                 }

            data_d['datasets'].append(my_dataset)

    return jsonify(data_d)


@app.route('/color_by_brand')
def colors_brands():
    # json to populate related brands from click on color slice on explorer
    a_color_hex = request.args.get('color_hex').lower()
    show_colors = Show_Color.query.join(Color).filter(a_color_hex == Color.color_hex).all()
    show_id_for_color = []
    brands = set()
    for x in show_colors:
        show_id_for_color.append(x.show_id)
    for show_id in show_id_for_color:
        brand = Brand.query.join(Show).filter(Show.show_id == show_id).one().brand_name
        brands.add(brand)

    return jsonify({'brands': list(brands)})


@app.route('/pie')
def pie():
    # json for the year/season/brand doughnut chart
    brand_id = request.args.get('brand_id')
    season = request.args.get('season')
    year = request.args.get('year')

    if brand_id == 'All':
        brand_id = []
        brands = Brand.query.all()
        for brand in brands:
            brand_id.append(brand.brand_id)
    else:
        brand_id = [brand_id]

    color_counter = []

    params = {
        'year': year,
        'season': season,
        'brand_id': None,
    }

    kwargs = params.copy()

    for key, value in params.iteritems():
        if value == 'All':
            del kwargs[key]

    for brand_id in brand_id:
        kwargs['brand_id'] = brand_id
        shows = Show.query.filter_by(**kwargs).all()

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


@app.route('/palette_chart')
def palette_chart():
    # json for the color explorer chart
    sorted_rainbow_hex = {'#808080': 137, '#ADFF2F': 76, '#FFB6C1': 1, '#556B2F': 77, '#FF8C00': 106, '#9932CC': 19, '#8A2BE2': 21, '#BA55D3': 17, '#2F4F4F': 52, '#00008B': 30, '#DB7093': 5, '#0000FF': 28, '#DC143C': 3, '#DDA0DD': 11, '#4169E1': 32, '#DA70D6': 9, '#DCDCDC': 133, '#7B68EE': 23, '#AFEEEE': 48, '#E6E6FA': 26, '#800080': 16, '#FFF5EE': 113, '#6B8E23': 79, '#FF69B4': 6, '#000080': 31, '#228B22': 71, '#008B8B': 53, '#5F9EA0': 45, '#EE82EE': 12, '#D3D3D3': 134, '#FF00FF': 14, '#48D1CC': 55, '#FFFFFF': 131, '#F5DEB3': 96, '#00FA9A': 60, '#F08080': 123, '#808000': 85, '#FAEBD7': 102, '#A9A9A9': 136, '#7FFFD4': 58, '#C0C0C0': 135, '#7FFF00': 74, '#FFEBCD': 100, '#B0C4DE': 34, '#008080': 54, '#FFFACD': 87, '#FFD700': 90, '#000000': 139, '#008000': 72, '#8B4513': 112, '#FFF0F5': 4, '#FFFFF0': 82, '#6A5ACD': 24, '#FFFAFA': 122, '#4682B4': 39, '#FFEFD5': 99, '#EEE8AA': 88, '#00FF00': 70, '#FFDEAD': 101, '#CD853F': 108, '#ADD8E6': 43, '#E0FFFF': 47, '#F8F8FF': 27, '#D8BFD8': 10, '#BC8F8F': 124, '#FF6347': 119, '#FF0000': 126, '#00CED1': 51, '#A0522D': 114, '#FFC0CB': 2, '#9370DB': 22, '#CD5C5C': 125, '#FFF8DC': 91, '#800000': 130, '#B8860B': 93, '#FFA07A': 115, '#40E0D0': 57, '#FAFAD2': 81, '#DEB887': 104, '#F0FFFF': 46, '#2E8B57': 64, '#E9967A': 118, '#87CEEB': 41, '#D2B48C': 103, '#90EE90': 66, '#00FFFF': 50, '#7CFC00': 75, '#FFE4E1': 120, '#BDB76B': 86, '#F4A460': 110, '#F0FFF0': 65, '#9400D3': 18, '#3CB371': 63, '#F5FFFA': 61, '#20B2AA': 56, '#1E90FF': 37, '#708090': 36, '#F5F5DC': 80, '#66CDAA': 59, '#9ACD32': 78, '#C71585': 8, '#F5F5F5': 132, '#32CD32': 69, '#8B0000': 129, '#696969': 138, '#191970': 29, '#8FBC8F': 68, '#00BFFF': 42, '#483D8B': 25, '#6495ED': 33, '#FFA500': 98, '#00FF7F': 62, '#A52A2A': 127, '#FAF0E6': 107, '#778899': 35, '#FFE4B5': 97, '#B22222': 128, '#DAA520': 92, '#4B0082': 20, '#FFFAF0': 94, '#B0E0E6': 44, '#F0E68C': 89, '#FFFF00': 84, '#006400': 73, '#FFE4C4': 105, '#FDF5E6': 95, '#8B008B': 15, '#FF7F50': 116, '#FFFFE0': 83, '#FA8072': 121, '#FFDAB9': 109, '#D2691E': 111, '#FF1493': 7, '#98FB98': 67, '#F0F8FF': 38, '#87CEFA': 40, '#FF4500': 117}

    s = sorted_rainbow_hex.items()
    order_color_hex = sorted(s, key=lambda x: x[1])
    color_order = []
    color_hex = []

    for order in order_color_hex:
        color_hex.append(order[0])
        color_order.append(order[1])

    x = color_hex
    data_color = color_order
    data_color = [10 for x in range(0, 137)]
    backgroundColor = color_hex
    hoverBackgroundColor = color_hex

    data = {
        'labels': color_hex,
        'datasets': [{
            'data': data_color,
            'backgroundColor': backgroundColor,
            'hoverBackgroundColor': hoverBackgroundColor
        }]
    }

    return jsonify(data)


if __name__ == "__main__":

    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
