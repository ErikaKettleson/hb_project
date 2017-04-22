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
    "Loewe": "/loewe", NO LOEWE FOR 2014 - STOPS @ 2013, PICKS UP AGAIN 2015
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



if match:
                url = match.group(1)

                if '_KOR_' in url and season == 'spring' and brand == 'Michael Kors':
                    image_urls.add(url)
                elif '_17G' in url and season == 'fall' and brand == 'Marc Jacobs':
                    image_urls.add(url)
                elif 'LUX_' in url and season == 'spring' and brand in ('Valentino', 'Marc Jacobs', 'Louis Vuitton'):
                    image_urls.add(url)
                elif 'VAL_' in url and season == 'fall' and brand == 'Valentino':
                    image_urls.add(url)
                if 'KIM_' in url and season == 'fall' and brand == 'Michael Kors':
                    image_urls.add(url)
                if '_KIM' in url and season == 'fall' and brand in ('Maison Margiela', 'Dolce Gabbana', 'Isabel Marant'):
                    image_urls.add(url)
                elif 'YSL_' in url and season == 'spring' and brand == 'Saint Laurent':
                    image_urls.add(url)
                elif 'BY8P' in url and season == 'fall' and brand == 'Saint Laurent':
                    image_urls.add(url)
                elif 'DRI_' in url and brand == 'Dries Van Noten':
                    image_urls.add(url)
                elif '_ON_' in url and brand in ('Proenza Schouler', 'Prada', 'Miu Miu', 'Givenchy', 'Celine', 'Balmain', 'Balenciaga'):
                    image_urls.add(url)
                elif '_ON_' in url and season == 'fall' and brand == 'Louis Vuitton':
                    image_urls.add(url)
                elif 'HER_' in url and brand == 'Hermes':
                    image_urls.add(url)
                elif 'CHA_' in url and brand == 'Chanel':
                    image_urls.add(url)
                elif 'DIO_' in url and brand == 'Christian Dior':
                    image_urls.add(url)
                elif 'MARC' in url and season == 'spring' and brand in ('Tory Burch', 'Altuzarra', 'Isabel Marant', 'Alexander McQueen', 'Maison Margiela', 'Oscar de la Renta', 'Missoni', 'Marni', 'Gucci'):
                    image_urls.add(url)
                elif 'MAR_' in url and season == 'fall' and brand == 'Marni':
                    image_urls.add(url)
                elif 'ALT_' in url and season == 'fall' and brand == 'Altuzarra':
                    image_urls.add(url)
                elif 'FEN_' in url and season == 'spring' and brand == 'Fendi':
                    image_urls.add(url)
                elif 'DOL_' in url and season == 'spring' and brand == 'Dolce Gabbana':
                    image_urls.add(url)
                elif 'GUC_' in url and season == 'fall' and brand == 'Gucci':
                    image_urls.add(url)
                elif 'AND_' in url and season == 'spring' and brand == 'J.W. Anderson':
                    image_urls.add(url)
                elif 'CDG_' in url and brand == 'Comme Des Garcons':
                    image_urls.add(url)
                elif '_ARC' in url and season == 'fall' and brand in ('Tory Burch', 'Christopher Kane', 'Oscar de la Renta', 'Missoni', 'J.W. Anderson', 'Fendi', 'Alexander McQueen'):
                    image_urls.add(url)
                elif 'christopher_kane_' in url and season == 'spring' and brand == 'Christopher Kane':
                    image_urls.add(url)

