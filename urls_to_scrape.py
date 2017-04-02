import re
import requests
from PIL import Image, ImageDraw, ImageColor, ImageFilter
from StringIO import StringIO
import os
import sys
from webcolors import *

years = [2017, 2016, 2015, 2014]
seasons = ['fall', 'spring']
brands = {"Acne Studios": "/acne-studios",
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

# urls_to_scrape = {}
urls_to_scrape = []

"""
      the dict looks something like this:
            urls = {
                  2017: {
                        "spring": {
                              "chanel": "some url",
                              "prada": "some url",
                        },
                        "summer": {
                              "chanel": "some url",
                              "prada": "some url",
                        },
                        "fall": {
                              "chanel": "some url",
                              "prada": "some url",
                        },
                  },
                  2016: {
                        "spring": {
                              "chanel": "some url",
                              "prada": "some url",
                        },
                        "summer": {
                              "chanel": "some url",
                              "prada": "some url",
                        },
                        "fall": {
                              "chanel": "some url",
                              "prada": "some url",
                        },
                  },
            }
      which i think might be as easy as

      x = { year: { season: { designer: 'http://www.vogue.com/fashion-shows/{}-{}-ready-to-wear{}'.format(season, year, designer_url) for designer, designer_url in designers.items() } for season in seasons } for year in years }

x = { year: { season: { designer: 'http://www.vogue.com/fashion-shows/{}-{}-ready-to-wear{}'.format(season, year, de
     ...: signer_url) for designer, designer_url in designers.items() } for season in seasons } for year in years 
"""
"""
      x gets passed into a function that loops through x and kickes get_urls for each, then passes each url to the pillow func
      which then writes everything to the database

"""


def feed_urls():
    generated_urls = {
        year: {
           season: {
                brand: 'http://www.vogue.com/fashion-shows/{}-{}-ready-to-wear{}'.format(season, year, brand_url)  # noqa E501
                for brand, brand_url in brands.items()
            } for season in seasons
        } for year in years
    }
    for url in generated_urls:
        show_urls = img_urls(url)


def img_urls(generated_url):
    image_urls = set()
    for url in urls_to_scrape:
        print "getting: %s" % url
        r = requests.get(url)
        if r.status_code == 200:
            print "got a hit!"
            html_body = r.text.split(",")
            for l in html_body:
                match = re.match(r'.*(http:.*/_(?!ARC|AG|UMB).*.jpg).*', l)
                # match = re.match(r'.*(http:\/\/assets.vogue.com\/photos\/.*\/master\/pass\/.*.[jpg|JPG]).*', l)
                if match:
                    image_urls.add(match.group(1))
                    # print match.group(1)
    return list(image_urls)

