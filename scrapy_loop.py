import scrapy
import re

# REVIEW SCRAPE



# *****************to loop through p blocks and append to a show list*****************
# ***********************************************************************************

# RETURNS REVIEW TEXT!
# scrapy shell 'http://www.vogue.com/fashion-shows/fall-2017-ready-to-wear/loewe'
# response.selector.xpath('//p/text()') 
# # RETURNS ALL P TAG data
# r = response.selector.xpath('//p/text()')[0] 
# # RETURNS FIRST REVIEW DATA CHUNK
# r.root 
# # RETURNS A BLOCK OF REVIEW!

# r = response.selector.xpath('//p/text()')
# remember enumerate!!! 
# text = []
# i = 0


# def loop(r):
#     for row in r:
#         # if i < 4:
#         text.append(r[i].root)
#         # i = i + 1

# whole URL: 'http://www.vogue.com/fashion-shows/SEASON-YEAR-ready-to-wear/DESIGNER'

years = [2017, 2016, 2015, 2014, 2013]
seasons = ['fall', 'spring']
designers = {"Acne Studios": "/acne-studios",
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
             "Céline": "/celine",
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
             "Hermès": "/hermes",
             "J.W. Anderson": "/j-w-anderson",
             "Junya Watanabe": "/junya-watanabe",
             "Kenzo": "/kenzo",
             "Lanvin": "/lanvin",
             "Loewe": "/loewe",
             "Louis Vuitton": "louis-vuitton",
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



# PSEUDO CODE loops

# base URL: 'http://www.vogue.com/fashion-shows/SEASON-YEAR-ready-to-wear/DESIGNER'

for year in years:
    for season in seasons:
        for designer in designers.values():
            get_review_body(response)
            get_image_url_list(response)


have a separate fxn that just serves the above loop with the designer page to then
use my regex fxn 

"def get_image_url_list(r or response.body()) url is passed from the above loop and it returns a list of image URLS"
WILL RETURN URLLIST

# BASE URL
# http://www.vogue.com/fashion-shows/fall-2017-ready-to-wear/DESIGNER-NAME/slideshow/collection

def get_image_url(response):
    # use regex to loop over the body of page to extract looks for each show
    image_urls = set()
    # rb is a big ol' str - also contains reveiw copy
    rb_split = response.body.split(',')
    for line in rb_split:
        match = re.match(r'.*(http:.*/_.*.jpg).*', line)
        if match:
            image_urls.add(match.group(1))
    # make a helper db seeding fxn (not here)
    # db.add(list(image_urls))


# DONE - get_review_body - takes as param a scrapy response
# "def get_review_body(also from response)"
# WILL RETURN BLOCK OF STRING REVIEW
# http://www.vogue.com/fashion-shows/fall-2017-ready-to-wear/DESIGNER-NAME-HERE
# ALL REVIEWS ON MAIN DESIGNER PAGE
# 'response' is feeding URL into scrapy

def get_review_body(response):
    # selector_list_review: returns a "scrapy.selector.unified.SelectorList"
    review = []
    review_selectors = response.selector.xpath('//p/text()')
    for selector in review_selectors:
        # returns a list of the review body
        review.append(selector.extract())
    print review
    # db.add(review)
