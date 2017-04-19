import requests
import re

show_url = "http://www.vogue.com/fashion-shows/spring-2017-ready-to-wear/loewe"
# spring 2016 tests:::: match = re.match(r'.*(http:.*/_(?!ARC|AG|UMB|A2X|GAS|MIC).*.jpg).*', l)
# altuzarra got 49/41 images - additional detail shots that dont hurt
# chanel got 109/100 images
# valentino got 100/91
# balmain got 69/60
# vetements got 45/42
# marni got 40/38
# Proenza Schouler got 46/41
# prada got 56/46
# dolce got 98/91
# gvenchy got 98/89 -some additional dolce show images m/w previous season
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# fall 2016 tests:::: match = re.match(r'.*(http:.*/_(?!ARC|AG|UMB|A2X|GAS|MIC).*.jpg).*', l)
# givenchy got 62/52
# altuzarra got 40/39 images 
# chanel got 102/94 images
# valentino got 91/82
# balmain got 69/60
# vetements got 56/53
# marni got BRKEN: 
    # working regex for marni::::  match = re.match(r'.*(http:\/\/assets.vogue.com\/photos\/.*\/master\/pass\/KIM.*.[jpg|JPG]).*', l)
    # with above line, get 42/39
# Proenza Schouler got 46/42
# prada got 56/53
# dolce got 104/97
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# spring 2015 tests
# givenchy got 62/58 with ::::: match = re.match(r'.*(.*http:.*_MON.*jpg).*', l)
# altuzarra got::::::: match = re.match(r'.*(.*http:.*KIM_.*jpg.*).*', l)
# chanel worked on::::::::: match = re.match(r'.*(.*http:.*CHA_.*jpg.*).*', l)
# valentino got match = re.match(r'.*(.*http:.*_MON.*jpg.*).*', l)
# balmain got 59/49 with::::: # match = re.match(r'.*(.*http:.*_MON.*jpg.*).*', l)

# vetements got perfecct with::::::: match = re.match(r'.*(.*http:.*Vetements.*jpg.*).*', l)
# marni got 49/46 with:::::: match = re.match(r'.*(.*http:.*MAR_.*jpg.*).*', l)
# Proenza Schouler 45/43 with ::::::::match = re.match(r'.*(http:.*/_(?!ARC|AG|UMB|A2X|GAS|MIC).*.jpg).*', l)

# prada got 53/46 with :::::: match = re.match(r'.*(http:.*/_(?!ARC|AG|UMB|A2X|GAS|MIC).*.jpg).*', l)
# dolce got 86/83 with ::::: match = re.match(r'.*(.*http:.*DOL_.*jpg.*).*', l)


def img_urls(show_url):
    # this returns a list of images for a show
    image_urls = set()

    # print "getting: %s" % show_url
    r = requests.get(show_url)
    if r.status_code == 200:
        print "got a hit!"
        html_body = r.text.split(",")
        for l in html_body:
            # below works on f/s 2017, spring 2016
            # match = re.match(r'.*(http:.*/_(?!ARC|AG|UMB|A2X|GAS|MIC).*.jpg).*', l)
            # below works for marni fall 2016
            # match = re.match(r'.*(http:\/\/assets.vogue.com\/photos\/.*\/master\/pass\/KIM.*.[jpg|JPG]).*', l)
            # below match works for Dolce spring 2015 (86/83)
            # match = re.match(r'.*(.*http:.*DOL_.*jpg.*).*', l)
            #below match works for marni spring 2015
            # match = re.match(r'.*(.*http:.*MAR_.*jpg.*).*', l)
            # below works for margiela spring 2017
            match = re.match(r'.*(.*http:.*_UMB.*jpg.*).*', l)
            # below works for vetements spring 2015
            # match = re.match(r'.*(.*http:.*Vetements.*jpg.*).*', l)
            # below for balmain spring 2015
            # match = re.match(r'.*(.*http:.*_MON.*jpg.*).*', l)
            # below for chanel spring 2015
            # match = re.match(r'.*(.*http:.*CHA_.*jpg.*).*', l)
            # below for altuzarra spring 2015
            # match = re.match(r'.*(.*http:.*KIM_.*jpg.*).*', l)
            # below for givenchy spring 2015
            # match = re.match(r'.*(.*http:.*_MON.*jpg.*).*', l)

            if match:
                image_urls.add(match.group(1))
    print "image urls:", image_urls
    print len(image_urls)
    # image_urls = list(image_urls)
    return list(image_urls)

img_urls(show_url)