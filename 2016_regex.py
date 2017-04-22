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
    "Loewe": "/loewe",
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

match = re.match(r'.*(http.*(?:KIM|KAN|_ALT|_MON|_CHA|celine-fall-2016-ready-to-wear|_CDG|_DIO|_CDG|_DOL|_FEN|_VAL|_GUC|_HER|_AG|_MAR|_KOR|_TOR|_OSC|_A2X|_MIS|_DRI|KIM|_ARC).*jpg).*', l)

if match:
                url = match.group(1)

                if 'KIM' in url and season == 'fall' and brand in ('Alexander McQueen', 'Christopher Kane', 'Isabel Marant', 'Louis Vuitton', 'Maison Margiela', 'Marni', 'Saint Laurent'):
                    image_urls.add(url)
                elif 'KAN' in url and season == 'spring' and brand == 'Christopher Kane':
                    image_urls.add(url)
                elif '_ALT' in url and season == 'fall' and brand == 'Altuzarra':
                    image_urls.add(url)
                elif '_MON' in url and brand in ('Balenciaga', 'Balmain', 'Givenchy', 'Miu Miu', 'Prada', 'Proenza Schouler'):
                    image_urls.add(url)
                elif '_MON' in url and season == 'spring' and brand == 'Celine':
                    image_urls.add(url)
                elif 'celine-fall-2016-ready-to-wear' in url and season == 'fall' and brand == 'Celine':
                    image_urls.add(url)
                elif '_CHA' in url and brand == 'Chanel':
                    image_urls.add(url)
                elif '_DIO' in url and brand == 'Christian Dior':
                    image_urls.add(url)
                elif '_CDG' in url and brand == 'Comme Des Garcons':
                    image_urls.add(url)
                elif '_DOL' in url and brand == 'Dolce Gabbana':
                    image_urls.add(url)
                elif '_FEN' in url and season == 'fall' and brand == 'Fendi':
                    image_urls.add(url)
                elif '_VAL' in url and brand == 'Valentino':
                    image_urls.add(url)
                elif '_GUC' in url and brand == 'Gucci':
                    image_urls.add(url)
                elif '_HER' in url and brand == 'Hermes':
                    image_urls.add(url)
                elif '_AG' in url and season == 'fall' and brand == 'J.W. Anderson':
                    image_urls.add(url)
                elif '_MAR' in url and season == 'spring' and brand == 'Marni':
                    image_urls.add(url)
                elif '_KOR' in url and brand == 'Michael Kors':
                    image_urls.add(url)
                elif '_TOR' in url and brand == 'Tory Burch':
                    image_urls.add(url)
                elif '_OSC' in url and brand == 'Oscar de la Renta':
                    image_urls.add(url)
                elif '_MON' in url and season == 'fall' and brand == 'Marc Jacobs':
                    image_urls.add(url)
                elif '_A2X' in url and season == 'spring' and brand in ('Marc Jacobs', 'Saint Laurent'):
                    image_urls.add(url)
                elif '_MIS' in url and season == 'fall' and brand == 'Missoni':
                    image_urls.add(url)
                elif 'KIM' in url and season == 'spring' and brand in ('Fendi', 'J.W. Anderson', 'Louis Vuitton', 'Maison Margiela', 'Missoni'):
                    image_urls.add(url)
                elif '_DRI' in url and season == 'spring' and brand == 'Dries Van Noten':
                    image_urls.add(url)
                elif '_ARC' in url and season == 'fall' and brand in ('Alexander McQueen', 'Dries Van Noten', 'Loewe'):
                    image_urls.add(url)
                elif '_ARC' in url and season == 'spring' and brand in ('Altuzarra', 'Isabel Marant', 'Loewe'):
                    image_urls.add(url)
