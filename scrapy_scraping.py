import scrapy

REVIEW: http://www.vogue.com/fashion-shows/fall-2017-ready-to-wear/loewe
DIV CLASS WREVIEW-CONTENT
LOOKS: http://www.vogue.com/fashion-shows/fall-2017-ready-to-wear/loewe/slideshow/collection#1
    - assets.vogue URL lives on the image src element - look at img class 

REVIEW CLASS: .review--content
FROM: http://www.vogue.com/fashion-shows/fall-2017-ready-to-wear/loewe

IMG URL CLASS: .gallery--center-module--image
FROM: http://www.vogue.com/fashion-shows/fall-2017-ready-to-wear/loewe/slideshow/collection#5


THESE LOOK PROMISING
>>> response.css('title')
[<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]

>>> response.css('title').extract()
['<title>Quotes to Scrape</title>']




RETURNS UGLY LOCATION/DATE
In [12]: response.css('.article-content--meta .meta--details .details--date').extract()
Out[12]: [u'<div class="details--date" data-reactid="110"><span data-reactid="111">PARIS, March 3, 2017</span></div>']


RETURNS REVIEW TEXT!
scrapy shell 'http://www.vogue.com/fashion-shows/fall-2017-ready-to-wear/loewe'
response.selector.xpath('//p/text()') RETURNS ALL P TAG data
r = response.selector.xpath('//p/text()')[0] RETURNS FIRST REVIEW DATA CHUNK
r.root RETURNS A BLOCK OF REVIEW!


# *****************to loop through p blocks and append to a show list*****************
# ***********************************************************************************

r = response.selector.xpath('//p/text()')
# remember enumerate!!! 
text = []
i = 0
for row in r:
    if i < 4:
        text.append(r[i].root)
        i = i + 1



class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    start_urls = [
        'http://www.vogue.com/fashion-shows/fall-2017-ready-to-wear/loewe',
    ]

    def parse(self, response):
        for quote in response.css('div.review--content'):
            yield {
                'placedate': quote.css('div.details--date').extract_first(),
                'text': quote.css('p.data').extract_first(),
            }

        # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)