import numpy as np
import random
from collections import namedtuple
from math import sqrt
from PIL import Image, ImageDraw, ImageColor, ImageFilter
import requests
from StringIO import StringIO
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils
from sqlalchemy import func
from model import Show, Show_Color, Brand, Color, connect_to_db, db
from server import app
import os
import sys
from webcolors import *

years = [2017]
seasons = ['fall', 'spring']
# brands = {"Carven": "/carven"}
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


Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))


def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points


def colorz(img, n=4):
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    print "rgbs", rgbs
    hex_codes = []
    color_names = []
    for rgb in rgbs:
        hex_codes.append(rgb_to_hex(rgb))
    print "hex codes", hex_codes
    for hex_code in hex_codes:
        color_names.append(hex_to_name(hex_codes))
    print "color names", color_names
    return rgbs
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
            smallest_distance = float('Inf') # infinity!!!
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

# GOT TO THUMBNAIL THE CROP BEFORE PROCESSINGS


def crop_image(img):
    # crop the image and background sample

    # print "hello at crop!"
    response = requests.get(img)
    img = Image.open(StringIO(response.content))

    width, height = img.size
    print width, height

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
    # LOE_crop = crop.save("loe_crop.jpg")
    # loe_bg_crop = bg_crop.save("loe_bg_crop.jpg")
    basewidth = 200
    wpercent = (basewidth/float(crop.size[0]))
    hsize = int((float(crop.size[1])*float(wpercent)))
    img = crop.resize((basewidth, hsize))

    colorz(img)

crop_image("http://assets.vogue.com/photos/58a110cd3decdb1c740dcc22/master/pass/_UMB2280.jpg")


# crop_image(img)
