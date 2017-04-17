import numpy as np
import random
from collections import namedtuple
from math import sqrt
import cv2
from PIL import Image, ImageDraw, ImageColor, ImageFilter
import requests
from StringIO import StringIO
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))


def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))


def colorz(img, n=5):
    # response = requests.get(filename)
    # img = Image.open(StringIO(response.content))
    # img = Image.open(filename)
    # img.thumbnail((450, 990))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    print "rgbs", rgbs
    return map(rtoh, rgbs)
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

    print clusters
    return clusters


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
    LOE_crop = crop.save("loe_crop.jpg")
    loe_bg_crop = bg_crop.save("loe_bg_crop.jpg")
    colorz(crop)

crop_image("http://assets.vogue.com/photos/58a110cd3decdb1c740dcc22/master/pass/_UMB2280.jpg")


# crop_image(img)
