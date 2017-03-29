from PIL import Image, ImageDraw, ImageColor, ImageFilter
import requests
from StringIO import StringIO
import os
import sys
from webcolors import *

# importing url - the hardcoded image returns the same results
# this is where 
response = requests.get('http://assets.vogue.com/photos/58b9348e61606a75f4402f3e/master/pass/_LOE0453.jpg')
img = Image.open(StringIO(response.content))

# img = Image.open("_UMB4717.jpg")
width, height = img.size
print width, height


def image_contents(img):
    # my_image = Image.open(img)

    print "format: ", img.format
    print "size: ", img.size
    print "mode: ", img.mode

    r, g, b = img.getpixel((1, 1))

    print "r:", r, "g:", g, "b", b

# image_contents(Image.open('bg_crop1.jpg'))


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
    # otherwise pillow errors out if it doesnt have the exact color name
    try:
        closest_name = actual_name = rgb_to_name(color)
    except ValueError:
        closest_name = closest_color(color)
        actual_name = None
    return actual_name, closest_name

    actual_name, closest_name = get_color_name(color)

    print "closest color name: ", closest_name


def get_colors(img, img2):
    # convert to palette format to getcolors, sort them & call get_color_name

    img = img.convert('P')
    img2 = img2.convert('P')

    bg_top_colors = sorted(img2.convert('RGB').getcolors(), reverse=True)[:20]
    top_colors = sorted(img.convert('RGB').getcolors(), reverse=True)[:15]
    print "bg colors:", bg_top_colors
    # print "main crop colors:", top_colors
    final_bg_colors = []
    final_colors = []

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
    print "final main colors w/o bg", final_colors[:5]
    final_colors = final_colors[:5]

    for color in final_colors:
        print "names:", get_color_name(color)


# get_colors(img)


def crop_image(img):
    # crop the image and background sample
    print "hello at crop!"

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
    crop.save("my_sweet7.jpg")
    bg_crop.save("bg_sweet_crop7.jpg")
    get_colors(crop, bg_crop)


crop_image(img)
