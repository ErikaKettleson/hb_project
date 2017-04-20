"""Utility file to seed database from pillow data/"""

# import datetime
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

years = [2017]
seasons = ['fall', 'spring']
# seasons = ['spring']
# brands = {
#           "Acne Studios": "/acne-studios",
#           "Loewe": "/loewe",
#           "Marc Jacobs": "/marc-jacobs",
#           "Oscar de la Renta": "/oscar-de-la-renta",
#           "Valentino": "/valentino"
#           }

brands = {
    "Acne Studios": "/acne-studios",
    "Alexander McQueen": "/alexander-mcqueen",
    "Alexander Wang": "/alexander-wang",
    "Altuzarra": "/altuzarra",
    "Ann Demeulemeester": "/ann-demeulemeester",
    "Antonio Berardi": "/antonio-berardi",
    "Balenciaga": "/balenciaga",
    "Balmain": "/balmain",
    "Carven": "/carven",
    "Celine": "/celine",
    "Chanel": "/chanel",
    "Christian Dior": "/christian-dior",
    "Christopher Kane": "/christopher-kane",
    "Comme Des Garcons": "/comme-des-garcons",
    "Isabel Marant": "/isabel-marant",
    "Dolce Gabbana": "/dolce-gabbana",
    "Dries Van Noten": "/dries-van-noten",
    "Fendi": "/fendi",
    "Giambattista Valli": "/giambattista-valli",
    "Givenchy": "/givenchy",
    "Gucci": "/gucci",
    "Hermes": "/hermes",
    "J.W. Anderson": "/j-w-anderson",
    "Junya Watanabe": "/junya-watanabe",
    "Kenzo": "/kenzo",
    "Lanvin": "/lanvin",
    "Loewe": "/loewe",
    "Louis Vuitton": "/louis-vuitton",
    "Maison Margiela": "/maison-martin-margiela",
    "Marc Jacobs": "/marc-jacobs",
    "Marni": "/marni",
    "Mary Katrantzou": "/mary-katrantzou",
    "Michael Kors": "/michael-kors-collection",
    "Miu Miu": "/miu-miu",
    "Missoni": "/missoni",
    "Oscar de la Renta": "/oscar-de-la-renta",
    "Prada": "/prada",
    "Proenza Schouler": "/proenza-schouler",
    "Roksanda": "/roksanda",
    "Stella McCartney": "/stella-mccartney",
    "Saint Laurent": "/saint-laurent",
    "Tory Burch": "/tory-burch",
    "Valentino": "/valentino",
    "Vetements": "/vetements",
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

# def show_colors(final_colors):
#     # A FXN TO AGGREGATE TOP COLORS BY SHOW
#     # final_colors is PER image, need to aggregate all final_colors to show colors
#     show_colors = []
#     for color in final_colors:
#         show_colors.append(color)

#     show_colors = final_colors[:6]
#     return show_colors


def get_color_name(color):
    # pillow errors out if it doesnt have the exact color name to rgb

    # print "at get_color_name"
    try:
        closest_name = actual_name = rgb_to_name(color)
    except ValueError:
        closest_name = closest_color(color)
        actual_name = None
    print closest_name
    return closest_name

    # actual_name, closest_name = get_color_name(color)

    # print "closest color name: ", closest_name
# get_color_name([231, 190, 56])


# def get_colors(img, img2):
#     # this function takes in bg & foreground colors and returns top img colors
#     # 1. convert image to palette format
#     img = img.convert('P')
#     img2 = img2.convert('P')

#     # 2. convert imgs to RGB for getcolors fxn - returns rgb tuples
#     bg_colors = (img2.convert('RGB').getcolors())
#     foreground_colors = (img.convert('RGB').getcolors())

#     # 3. set up our lists to capture top colors for bg & foreground
#     final_bg_colors = []
#     final_colors = []
#     # 4. set up empty list to capture named final colors
#     final_named_colors = []

#     named_bg_colors = []
#     named_foreground_colors = []

#     # 6. these two loops return lists of named colors
#     for count, rgb in bg_colors:
#         named_bg_colors.append(get_color_name(rgb))
#     for count, rgb in foreground_colors:
#         named_foreground_colors.append(get_color_name(rgb))

#     # 7. these create color/count pairs 
#     count_bg_colors = {color: named_bg_colors.count(color) for color in named_bg_colors}
#     count_foreground_colors = {color: named_foreground_colors.count(color) for color in named_foreground_colors}

#     # 8. these take the color/count pairs and sort them
#     sorted_bg_colors = sorted(count_foreground_colors.items(), key=lambda x: x[1], reverse=True)[:10]
#     sorted_foreground_colors = sorted(count_foreground_colors.items(), key=lambda x: x[1], reverse=True)[:10]

#     # 9. next i have to append top bg colors to final_bg_colors to compare foreground againsr
#     final_bg_colors.append(sorted_bg_colors)

#     # 10. next i need to compare the fg colors against bg colors & append to the fg final color list

#     for color, count in sorted_foreground_colors:
#         if color not in final_bg_colors:
#             final_colors.append(color)
#         else:
#             pass

#     final_named_colors = final_colors[:10]

#     return final_named_colors


Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))


def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points


def colorz(url, n=4):
    print "URL::::", url
    img = crop_image(url)
    w, h = img.size
    print w, h
    print "at colorz"

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    # print "rgbs", rgbs
    # hex_codes = []
    named_colors = []
    # for rgb in rgbs:
        # hex_codes.append(rgb_to_hex(rgb))
    # print "hex codes", hex_codes
    # for hex_code in hex_codes:
        # color_names.append(hex_to_name(hex_codes))
    # print "color names", color_names
    for rgb in rgbs:
        named_colors.append(get_color_name(rgb))
    # for name in named_colors:
    #     hex_codes.append(name_to_hex(name))
    # print "hex:", hex_codes, "named:", named_colors
    return named_colors

# import ipdb; ipdb.set_trace()


def euclidean(p1, p2):
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
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
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

    # print clusters
    return clusters


def crop_image(url):
    # crop the image and background sample

    print "hello at crop!"
    response = requests.get(url)
    img = Image.open(StringIO(response.content))

    width, height = img.size
    # 2000 width, 3000 height...so 600 x 450

    left_box = ((.30) * width)
    top_box = ((.15) * height)
    width_box = ((.35) * width)
    height_box = ((.66) * height)
    box = (left_box, top_box, left_box+width_box, top_box+height_box)
    # print "box", box

    # left_bg = ((0) * width)
    # top_bg = ((0) * height)
    # width_bg = ((.25) * width)
    # height_bg = ((.75) * height)
    # bg_box = (left_bg, top_bg, left_bg+width_bg, top_bg+height_bg)
    # print "bg_box", bg_box

    crop = img.crop(box)
    # bg_crop = img.crop(bg_box)
    # LOE_crop = crop.save("loe_crop.jpg")
    # loe_bg_crop = bg_crop.save("loe_bg_crop.jpg")
    basewidth = 200
    wpercent = (basewidth/float(crop.size[0]))
    hsize = int((float(crop.size[1])*float(wpercent)))
    img = crop.resize((basewidth, hsize))

    return img


def img_urls(show_url, brand, season):
    # this returns a list of images for a show
    image_urls = set()

    # print "getting: %s" % show_url
    r = requests.get(show_url)
    if r.status_code == 200:
        print "got a hit!"
        html_body = r.text.split(",")
        for l in html_body:
            match = re.match(r'.*(http.*(?:MAR|UMB|KIM|ALT|ARC|ALE|L7A|MON|BOT|CHA|DIO|CDG|DOL|FEN|VAL|GUC|HER|AG|WAT|MAR|KOR|KEN|STE|GIA|KAT|JUN|ROK|TEN|YSL|LUC|VET|WAN|LLL).*jpg).*', l)
            # match = re.match(r'.*(.*http:.*_MAR.*jpg.*).*', l)
            # match = re.match(r'.*(http:.*/_(?!ARC|AG|UMB|A2X|GAS|MIC).*.jpg).*', l)
            # match = re.match(r'.*(http:\/\/assets.vogue.com\/photos\/.*\/master\/pass\/.*.[jpg|JPG]).*', l)
            if match:
                url = match.group(1)

                if '_UMB' in url and season == 'spring' and brand in ('Valentino', 'Acne Studios', 'Loewe', 'Marc Jacobs', 'Oscar de la Renta'):
                    image_urls.add(url)
                elif 'KIM' in url and season == 'spring' and brand in ('Alexander McQueen', 'Antonio Berardi', 'Christopher Kane', 'Marc Jacobs', 'Louis Vuitton', 'Isabel Marant', 'Dries Van Noten', 'Kenzo', 'Lanvin', 'Mary Katrantzou', 'Missoni'):
                    image_urls.add(url)
                elif '_ALE' in url and season == 'spring' and brand == 'Alexander Wang':
                    image_urls.add(url)
                elif '_ALT' in url and season == 'spring' and brand == 'Altuzarra':
                    image_urls.add(url)
                elif '_L7A' in url and season == 'spring' and brand == 'Ann Demeulemeester':
                    image_urls.add(url)
                elif '_MON' in url and season == 'spring' and brand in ('Balenciaga', 'Balmain', 'Celine', 'Givenchy', 'Miu Miu', 'Prada', 'Proenza Schouler'):
                    image_urls.add(url)
                elif '_BOT' in url and season == 'spring' and brand == 'Bottega Veneta':
                    image_urls.add(url)
                elif '_CHA' in url and brand == 'Chanel':
                    image_urls.add(url)
                elif '_DIO' in url and brand == 'Christian Dior':
                    image_urls.add(url)
                elif '_CDG' in url and season == 'spring' and brand == 'Comme Des Garcons':
                    image_urls.add(url)
                elif '_DOL' in url and brand == 'Dolce Gabbana':
                    image_urls.add(url)
                elif '_FEN' in url and season == 'spring' and brand == 'Fendi':
                    image_urls.add(url)
                elif '_VAL' in url and season == 'spring' and brand == 'Giambattista Valli':
                    image_urls.add(url)
                elif '_GUC' in url and brand == 'Gucci':
                    image_urls.add(url)
                elif '_HER' in url and brand == 'Hermes':
                    image_urls.add(url)
                elif '_AG' in url and season == 'spring' and brand == 'J.W. Anderson':
                    image_urls.add(url)
                elif '_WAT' in url and season == 'spring' and brand == 'Junya Watanabe':
                    image_urls.add(url)
                elif '_MAR' in url and season == 'spring' and brand in ('Maison Margiela', 'Marni'):
                    image_urls.add(url)
                elif '_KOR' in url and brand == 'Michael Kors':
                    image_urls.add(url)
                elif '_LUC' in url and season == 'spring' and brand in ('Tory Burch', 'Roksanda'):
                    image_urls.add(url)
                elif '_STE' in url and season == 'spring' and brand == 'Stella McCartney':
                    image_urls.add(url)
                elif '_YSL' in url and brand == 'Saint Laurent':
                    image_urls.add(url)
                elif '_VET' in url and season == 'spring' and brand == 'Vetements':
                    image_urls.add(url)
                elif '_UMB' in url and season == 'fall' and brand in ('Acne Studios', 'Altuzarra', 'Isabel Marant', 'Louis Vuitton', 'Marc Jacobs', 'Stella McCartney'):
                    image_urls.add(url)
                elif 'KIM' in url and season == 'fall' and brand in ('Alexander McQueen', 'Christopher Kane', 'Antonio Berardi', 'Comme Des Garcons', 'Dries Van Noten', 'Fendi', 'J.W. Anderson', 'Lanvin', 'Loewe'):
                    image_urls.add(url)
                elif '_WAN' in url and season == 'fall' and brand == 'Alexander Wang':
                    image_urls.add(url)
                elif '_LLL' in url and season == 'fall' and brand == 'Ann Demeulemeester':
                    image_urls.add(url)
                elif '_MON' in url and season == 'fall' and brand in ('Balenciaga', 'Balmain', 'Celine', 'Miu Miu', 'Prada', 'Proenza Schouler'):
                    image_urls.add(url)
                elif '_GIA' in url and season == 'fall' and brand == 'Giambattista Valli':
                    image_urls.add(url)
                elif '_KEN' in url and season == 'fall' and brand == 'Kenzo':
                    image_urls.add(url)
                elif '_MAR' in url and season == 'fall' and brand in ('Marni', 'Maison Margiela'):
                    image_urls.add(url)
                elif '_KAT' in url and season == 'fall' and brand == 'Mary Katrantzou':
                    image_urls.add(url)
                elif '_ROK' in url and season == 'fall' and brand == 'Roksanda':
                    image_urls.add(url)
                elif '_TEN' in url and season == 'fall' and brand == 'Oscar de la Renta':
                    image_urls.add(url)
                elif '_ARC' in url and season == 'fall' and brand in ('Missoni', 'Tory Burch', 'Vetements'):
                    image_urls.add(url)
                elif '_VAL' in url and season == 'fall' and brand == 'Valentino':
                    image_urls.add(url)





    # print "image urls:", image_urls
    # print len(image_urls)
    # image_urls = list(image_urls)
    print "IMAGE URLS:", list(image_urls)
    return list(image_urls)
    # pillow_loop(image_urls)


def feed_urls():
    # main fxn to call url generator and aggregate top colors by show
    generated_urls = {year: {season: {brand: 'http://www.vogue.com/fashion-shows/{}-{}-ready-to-wear{}'.format(season, year, brand_url) for brand, brand_url in brands.items()} for season in seasons} for year in years}
    # print "generated urls:", generated_urls
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
                # print "top_show_colors", top_show_colors, type(top_show_colors)
                
                load_show_colors(top_show_colors, show)
                # print top_show_colors, brand, year, season 
                # import ipdb; ipdb.set_trace()
    # FIXME:
    # return top_show_colors, brand, year, season

            # just have to pass top show color & show (or just show.show_id)


def load_brands(brands):
    """Load brands into database."""

    print "Brands"

    for key, value in brands.items():
        brand_name = key

        brand = Brand(brand_name=brand_name)

    # We need to add to the session or it won't ever be stored
        db.session.add(brand)

    # Once we're done, we should commit our work
    db.session.commit()


def load_colors():
    """Load colors/hex from css3 dict into database."""

    print "Color"

    for key, value in css3_hex_to_names.items():
        color_hex, color_name = key, value
        color = Color(color_hex=color_hex,
                      color_name=color_name)

        db.session.add(color)

    # Once we're done, we should commit our work
    db.session.commit()


def load_show(year, season, brand):
    """Load shows into database."""

    print "Show"

    brand_id = db.session.query(Brand).filter_by(brand_name=brand).one().brand_id

    year = 2017
    show = Show(season=season,
                year=year,
                brand_id=brand_id)

    # We need to add to the session or it won't ever be stored
    db.session.add(show)

    # Once we're done, we should commit our work
    db.session.commit()
    return show


def load_show_colors(top_show_colors, show):
    """Set value for each shows top colors & seed """

    # show_id = db.session.query(Show.season == season,
    #                            Show.year == year,
    #                            (Show.brands.brand_name == brand)).one().show_id

    # show_id = db.session.query(Show).join(Brand).filter(Show.season == season).\
    #                                                     filter(Show.year == year).\
    #                                                     filter(Brand.brand_name == brand).one().show_id
    # db.session.add(show_id)
    show_id = show.show_id

    # color_id = db.session.query(Color.color_name == (color for colors in top_show_colors)).one().color_id

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

    load_brands(brands)
    load_colors()
    # top_show_colors, brand, year, season = feed_urls()
    feed_urls()
    # year = 2017
    # load_show(year, season, brand)
    # load_show_colors(top_show_colors, brand, year, season)
