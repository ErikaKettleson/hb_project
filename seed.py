
from sqlalchemy import func
from collections import namedtuple
from model import Show, Show_Color, Brand, Color, connect_to_db, db
from server import app
from StringIO import StringIO
from math import sqrt
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw, ImageColor, ImageFilter
import requests
import numpy as np
import os
import random
import sys
from webcolors import *

years = [2013]
seasons = ['fall', 'spring']

brands = {
    "Alexander McQueen": "/alexander-mcqueen",
    "Altuzarra": "/altuzarra",
    "Balenciaga": "/balenciaga",
    "Balmain": "/balmain",
    "Celine": "/celine",
    "Chanel": "/chanel",
    "Christian Dior": "/christian-dior",
    "Christopher Kane": "/christopher-kane",
    "Comme Des Garcons": "/comme-des-garcons",
    "Isabel Marant": "/isabel-marant",
    "Dolce Gabbana": "/dolce-gabbana",
    "Dries Van Noten": "/dries-van-noten",
    "Fendi": "/fendi",
    "Givenchy": "/givenchy",
    "Gucci": "/gucci",
    "Hermes": "/hermes",
    "J.W. Anderson": "/j-w-anderson",
    "Louis Vuitton": "/louis-vuitton",
    "Maison Margiela": "/maison-martin-margiela",
    "Marc Jacobs": "/marc-jacobs",
    "Marni": "/marni",
    "Michael Kors": "/michael-kors-collection",
    "Miu Miu": "/miu-miu",
    "Missoni": "/missoni",
    "Oscar de la Renta": "/oscar-de-la-renta",
    "Prada": "/prada",
    "Proenza Schouler": "/proenza-schouler",
    "Saint Laurent": "/saint-laurent",
    "Tory Burch": "/tory-burch",
    "Valentino": "/valentino",
}


def closest_color(color):
    # buckets the colors to convert colors from rgb to css friendly names

    min_colors = {}

    # loops over css3 named hex/color items (138 pairs)
    # next, pull r, g, b, values from image color tuple
    # then convert hex to rgb with just key (hex values)

    for key, name in css3_hex_to_names.items():
        r_c, g_c, b_c = hex_to_rgb(key)
        # an example might be 124 125 0
        # so r = (124 - color[0]) ^ 2
        # color is the inputted rgb value tuples

        r = (r_c - color[0]) ** 2
        g = (g_c - color[1]) ** 2
        b = (b_c - color[2]) ** 2

        min_colors[(r + g + b)] = name
        # print "MIN COLORS", min_colors
        # print "MIN KEYS ONLY", min_colors[min(min_colors.keys())]
    return min_colors[min(min_colors.keys())]


def get_color_name(color):
    # pillow errors out if it doesnt have the exact color name to rgb
    try:
        closest_name = actual_name = rgb_to_name(color)
    except ValueError:
        closest_name = closest_color(color)
        actual_name = None
    print closest_name
    return closest_name

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

# k-means cluster algorithm from this blog post:
#http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/


def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points


def colorz(url, n=4):
    # returns the 4 colors (n=4) by name
    # pre-process image with crop_image, call point/cluster fxns
    print "URL::::", url
    img = crop_image(url)
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]

    named_colors = []

    for rgb in rgbs:
        named_colors.append(get_color_name(rgb))

    return named_colors


def euclidean(p1, p2):
    # squared in order to place more weight on points that are farther from k
    # called by kmeans, returns distance from points to the randon k cluster
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))


def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)


def kmeans(points, k, min_diff):
    # n observations into k clusters
    # returns clusters to the euclidian distance fxn
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            # unbounded upper value for comparison
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters


def crop_image(url):
    # crop the image for quicker analysis and background sample

    print "hello at crop!"
    response = requests.get(url)
    img = Image.open(StringIO(response.content))

    width, height = img.size
    # 2000 width, 3000 height...so will be ~ 600 x 450/image

    left_box = ((.30) * width)
    top_box = ((.15) * height)
    width_box = ((.35) * width)
    height_box = ((.66) * height)
    box = (left_box, top_box, left_box+width_box, top_box+height_box)

    crop = img.crop(box)

    basewidth = 200
    wpercent = (basewidth/float(crop.size[0]))
    hsize = int((float(crop.size[1])*float(wpercent)))
    img = crop.resize((basewidth, hsize))

    return img


def img_urls(show_url, brand, season):
    # this returns a list of image urls for a show with regex feeding sort logic
    image_urls = set()

    r = requests.get(show_url)
    if r.status_code == 200:
        print "got a hit!"
        html_body = r.text.split(",")
        for l in html_body:
            match = re.match(r'.*(http.*(?:_D7Q|_MG_|_J9D|MIS_|KOR_|_KOR|_CDG|_ARC|MAR_|_MAR|CDG_|GUC_|_THO|_GVC|_MMM|_OSC|VAL_|_AG|MJA_|DRI_|NOT_|_ISA|HER_|_ON_|CHA_|VUI_|FIO_|ALT_|_ALT|FEN_|_FEN|_DOL|DEG_).*(?:jpg|JPG)).*', l)

            if match:
                url = match.group(1)

                if '_D7Q' in url and season == 'fall' and brand == 'Alexander McQueen':
                    image_urls.add(url)
                elif 'GUC_' in url and season == 'spring' and brand == 'Gucci':
                    image_urls.add(url)
                elif '_THO' in url and season == 'spring' and brand == 'Tory Burch':
                    image_urls.add(url)
                elif '_GVC' in url and season == 'fall' and brand in ('Gucci'):
                    image_urls.add(url)
                elif '_MMM' in url and brand == 'Maison Margiela':
                    image_urls.add(url)
                elif '_OSC' in url and brand == 'Oscar de la Renta':
                    image_urls.add(url)
                elif 'VAL_' in url and brand == 'Valentino':
                    image_urls.add(url)
                elif '_AG' in url and season == 'fall' and brand == 'Marc Jacobs':
                    image_urls.add(url)
                elif 'MJA_' in url and season == 'spring' and brand == 'Marc Jacobs':
                    image_urls.add(url)
                if 'DRI_' in url and season == 'fall' and brand in ('Dries Van Noten'):
                    image_urls.add(url)
                elif 'NOT_' in url and season == 'spring' and brand == 'Dries Van Noten':
                    image_urls.add(url)
                elif '_ISA' in url and season == 'fall' and brand == 'Isabel Marant':
                    image_urls.add(url)
                elif 'HER_' in url and brand == 'Hermes':
                    image_urls.add(url)
                elif '_ON_' in url and brand in ('Balenciaga', 'Balmain', 'Celine'):
                    image_urls.add(url)
                elif '_ON_' in url and season == 'spring' and brand in ('Alexander McQueen', 'Givenchy', 'Isabel Marant', 'Proenza Schouler', 'Saint Laurent'):
                    image_urls.add(url)
                elif '_ON_' in url and season == 'fall' and brand in ('Christian Dior', 'Miu Miu'):
                    image_urls.add(url)
                elif 'CHA_' in url and brand == 'Chanel':
                    image_urls.add(url)
                elif 'VUI_' in url and brand == 'Louis Vuitton':
                    image_urls.add(url)
                elif 'FIO_' in url and season == 'fall' and brand == 'Loewe':
                    image_urls.add(url)
                elif 'ALT_' in url and season == 'spring' and brand == 'Altuzarra':
                    image_urls.add(url)
                elif '_ALT' in url and season == 'fall' and brand == 'Altuzarra':
                    image_urls.add(url)
                elif 'FEN_' in url and season == 'spring' and brand == 'Fendi':
                    image_urls.add(url)
                elif '_FEN' in url and season == 'fall' and brand == 'Fendi':
                    image_urls.add(url)
                elif '_DOL' in url and season == 'fall' and brand == 'Dolce Gabbana':
                    image_urls.add(url)
                elif 'DEG_' in url and season == 'spring' and brand == 'Dolce Gabbana':
                    image_urls.add(url)
                elif '_MG_' in url and season == 'spring' and brand in ('Christopher Kane', 'J.W. Anderson', 'Loewe', 'Miu Miu'):
                    image_urls.add(url)
                elif 'CDG_' in url and season == 'spring' and brand == 'Comme Des Garcons':
                    image_urls.add(url)
                elif '_CDG' in url and season == 'fall' and brand == 'Comme Des Garcons':
                    image_urls.add(url)
                elif '_ARC' in url and season == 'fall' and brand in ('Christopher Kane', 'Givenchy', 'J.W. Anderson', 'Missoni', 'Proenza Schouler', 'Saint Laurent', 'Tory Burch'):
                    image_urls.add(url)
                elif 'MAR_' in url and season == 'spring' and brand == 'Marni':
                    image_urls.add(url)
                elif '_MAR' in url and season == 'fall' and brand == 'Marni':
                    image_urls.add(url)
                elif 'MIS_' in url and season == 'spring' and brand == 'Missoni':
                    image_urls.add(url)
                elif 'KOR_' in url and season == 'spring' and brand == 'Michael Kors':
                    image_urls.add(url)
                elif '_KOR' in url and season == 'fall' and brand == 'Michael Kors':
                    image_urls.add(url)
                elif '_J9D' in url and season == 'fall' and brand == 'Prada':
                    image_urls.add(url)
                elif '_MG_' in url and season == 'spring' and brand == 'Prada':
                    image_urls.add(url)

    print "IMAGE URLS:", list(image_urls)
    return list(image_urls)


def feed_urls():
    # main fxn to call url generator and aggregate top colors by show
    generated_urls = {year: {season: {brand: 'http://www.vogue.com/fashion-shows/{}-{}-ready-to-wear{}'.format(season, year, brand_url) for brand, brand_url in brands.items()} for season in seasons} for year in years}

    for year in generated_urls.keys():
        for season in generated_urls[year].keys():
            for brand, brand_url in generated_urls[year][season].items():
                print "generated urls", generated_urls
                print "brand url:", brand_url
                print "season", season
                print "brand name:", brand
                show = load_show(year, season, brand)
                image_urls = img_urls(brand_url, brand, season)

                top_show_colors = []
                final_colors_for_show = []
                neutral_colors = ['silver', 'whitesmoke', 'lightgrey', 'darkgray', 'gainsboro', 'dimgrey', 'linen', 'silver']
                for url in image_urls:
                    final_named_colors = []
                    try:
                        final_named_colors = colorz(url)
                    except Exception as e:
                        print str(e)

                    for color in final_named_colors:
                        top_show_colors.append(color)
                print "at feed urls, top show colors: ", top_show_colors

                count_colors = {color: top_show_colors.count(color) for color in top_show_colors}
                ranked_show_colors = sorted(set(top_show_colors), key=count_colors.get, reverse=True)
                for color in ranked_show_colors:
                    if color not in neutral_colors:
                        final_colors_for_show.append(color)

                top_show_colors = final_colors_for_show[:10]

                load_show_colors(top_show_colors, show)


def load_brands(brands):
    """Load brands into database."""

    print "Brands"

    for key, value in brands.items():
        brand_name = key

        brand = Brand(brand_name=brand_name)

        db.session.add(brand)

    db.session.commit()


def load_colors():
    """Load colors/hex from css3 dict into database."""

    print "Color"

    for key, value in css3_hex_to_names.items():
        color_hex, color_name = key, value
        color = Color(color_hex=color_hex,
                      color_name=color_name)

        db.session.add(color)

    db.session.commit()


def load_show(year, season, brand):
    """Load shows into database."""

    print "Show"

    brand_id = db.session.query(Brand).filter_by(brand_name=brand).one().brand_id

    year = 2013
    show = Show(season=season,
                year=year,
                brand_id=brand_id)

    # We need to add to the session or it won't ever be stored
    db.session.add(show)

    # Once we're done, we should commit our work
    db.session.commit()
    return show


def load_show_colors(top_show_colors, show):

    show_id = show.show_id

    for color in top_show_colors:
        print "color: ", color
        color_id = db.session.query(Color).filter(Color.color_name == color).one().color_id
        print "color_id:", color_id
        show_color = Show_Color(show_id=show_id, color_id=color_id)
        db.session.add(show_color)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # load_brands(brands)
    # load_colors()
    feed_urls()

    # load_show(year, season, brand)
    # load_show_colors(top_show_colors, brand, year, season)
