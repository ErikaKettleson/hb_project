"""Utility file to seed database from pillow data/"""

import datetime
from sqlalchemy import func

from model import Show, Show_Color, Brand, Image, Color, connect_to_db, db
from server import app

from PIL import Image, ImageDraw, ImageColor, ImageFilter
import requests
from StringIO import StringIO
import os
import sys
from webcolors import *

years = [2017]
seasons = ['fall', 'spring']
# brands = {"Altuzarra": "/altuzarra"}
brands = {
    "Acne Studios": "/acne-studios",
    "Alexander McQueen": "/alexander-mcqueen",
    "Alexander Wang": "/alexander-wang",
    "Altuzarra": "/altuzarra",
    "Ann Demeulemeester": "/ann-demeulemeester",
    "Antonio Berardi": "/antonio-berardi",
    "Balenciaga": "/balenciaga",
    "Balmain": "/balmain",
    "Bottega Veneta": "/bottega-veneta",
    "Calvin Klein": "/calvin-klein",
    "Carven": "/carven",
    "Celine": "/celine",
    "Chanel": "/chanel",
    "Christian Dior": "/christian-dior",
    "Christopher Kane": "/christopher-kane",
    "Comme Des Garcons": "/comme-des-garcons",
    "Derek Lam": "/derek-lam",
    "Isabel Marant": "/isabel-marant",
    "Dolce Gabbana": "/dolce-gabbana",
    "Dries Van Noten": "/dries-van-noten",
    "Etro": "/etro",
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




def image_contents(img):

    print "format: ", img.format
    print "size: ", img.size
    print "mode: ", img.mode

    r, g, b = img.getpixel((1, 1))

    print "r:", r, "g:", g, "b", b


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

    print "at get_color_name"
    try:
        closest_name = actual_name = rgb_to_name(color)
    except ValueError:
        closest_name = closest_color(color)
        actual_name = None
    return closest_name

    actual_name, closest_name = get_color_name(color)

    # print "closest color name: ", closest_name


def get_colors(img, img2):
    # convert to palette format to getcolors, sort & call get_color_name

    img = img.convert('P')
    img2 = img2.convert('P')

    bg_top_colors = sorted(img2.convert('RGB').getcolors(), reverse=True)[:20]
    top_colors = sorted(img.convert('RGB').getcolors(), reverse=True)[:15]
    print "bg colors:", bg_top_colors
    final_bg_colors = []
    final_colors = []
    final_named_colors = []

    i = 0
    for count, rgb in bg_top_colors:
        top_bg_rgb = bg_top_colors[i][1]
        final_bg_colors.append(top_bg_rgb)
        i = i + 1

    i = 0
    for count, rgb in top_colors:
        top_rgb = top_colors[i][1]
        i = i + 1
        if top_rgb not in top_bg_rgb:
            final_colors.append(top_rgb)
        else:
            pass
    print "final main colors w/o bg", final_colors[:6]
    final_colors = final_colors[:6]

    for color in final_colors:
        named_color = get_color_name(color)
        final_named_colors.append(named_color)
    return final_named_colors

    # return final_colors
    # print type(final_colors)
    # show_colors(final_colors)
    # call the show colors fxn here to get top colors for overall show


def crop_image(img):
    # crop the image and background sample

    print "hello at crop!"

    width, height = img.size

    left_box = ((.30) * width)
    top_box = ((.15) * height)
    width_box = ((.45) * width)
    height_box = ((.66) * height)
    box = (left_box, top_box, left_box+width_box, top_box+height_box)
    print "box", box

    left_bg = ((0) * width)
    top_bg = ((0) * height)
    width_bg = ((.25) * width)
    height_bg = ((.75) * height)
    bg_box = (left_bg, top_bg, left_bg+width_bg, top_bg+height_bg)
    print "bg_box", bg_box

    crop = img.crop(box)
    bg_crop = img.crop(bg_box)
    return get_colors(crop, bg_crop)


def pillow_loop(img_urls):
    # for url in img_urls:
    print "URL:", img_urls
    response = requests.get(img_urls)
    img = Image.open(StringIO(response.content))
    print "heading to crop"
    return crop_image(img)


def img_urls(show_url):
    # this returns a list of images for a show
    image_urls = set()

    print "getting: %s" % show_url
    r = requests.get(show_url)
    if r.status_code == 200:
        print "got a hit!"
        html_body = r.text.split(",")
        for l in html_body:
            match = re.match(r'.*(http:.*/_(?!ARC|AG|UMB).*.jpg).*', l)
            # match = re.match(r'.*(http:\/\/assets.vogue.com\/photos\/.*\/master\/pass\/.*.[jpg|JPG]).*', l)
            if match:
                image_urls.add(match.group(1))
    print "image urls:", image_urls
    # print len(image_urls)
    # image_urls = list(image_urls)
    return list(image_urls)
    # pillow_loop(image_urls)


def feed_urls():
    # main fxn to call url generator and aggregate top colors by show
    generated_urls = {year: {season: {brand: 'http://www.vogue.com/fashion-shows/{}-{}-ready-to-wear{}'.format(season, year, brand_url) for brand, brand_url in brands.items()} for season in seasons} for year in years}
    print "generated urls:", generated_urls
    for year in generated_urls.keys():
        for season in generated_urls[year].keys():
            for brand, brand_url in generated_urls[year][season].items():
                print "generated urls", generated_urls
                print "brand url:", brand_url
                print "brand name:", brand
                image_urls = img_urls(brand_url)

                top_show_colors = []
                for url in image_urls:
                    final_named_colors = pillow_loop(url)
                    print "at feed urls, final colors: ", final_named_colors
                    for color in final_named_colors:
                        top_show_colors.append(color)
                count_colors = {color: top_show_colors.count(color) for color in top_show_colors}
                top_show_colors = sorted(set(top_show_colors), key=count_colors.get, reverse=True)
                print "TOP SHOW COLORS: ", top_show_colors[:10]

                # print "show colors", show_colors
                # call a db adding fxn here, pass in show_colors, season, year, brand
                # db.add stuff in here


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


def load_show(seasons, years, brand):
    """Load shows into database."""

    print "Show"

    season = season for season in seasons
    year = year for year in years
    brand_id = query.filter(Brand.brand_name == brand)
    # NEED TO ADD BRAND_ID, NOT BRAND_NAME...

    show = Show(season=season,
                year=year,
                brand_id=brand_id)

    # We need to add to the session or it won't ever be stored
    db.session.add(show)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    feed_urls()
