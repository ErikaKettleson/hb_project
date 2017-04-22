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



if match:
                url = match.group(1)

                if 'KIM' in url and season == 'spring' and brand == 'Altuzarra':
                    image_urls.add(url)
                elif 'OSC_' in url and season == 'fall' and brand == 'Oscar de la Renta':
                    image_urls.add(url)
                elif 'LUX_' in url and season == 'spring' and brand == 'Oscar de la Renta':
                    image_urls.add(url)
                if 'KIM' in url and season == 'fall' and brand in ('Christopher Kane', 'Marni'):
                    image_urls.add(url)
                elif 'CHA' in url and season == 'spring' and brand == 'Chanel':
                    image_urls.add(url)
                elif 'chanel' in url and season == 'fall' and brand == 'Chanel':
                    image_urls.add(url)
                elif 'ALT' in url and season == 'fall' and brand == 'Altuzarra':
                    image_urls.add(url)
                elif '_MON' in url and season == 'spring' and brand in ('Balenciaga', 'Givenchy'):
                    image_urls.add(url)
                elif '_ON_' in url and season == 'spring' and brand == 'Proenza Schouler':
                    image_urls.add(url)
                elif '_MON' in url and season == 'fall' and brand == 'Proenza Schouler':
                    image_urls.add(url)
                elif '_HER' in url and season == 'spring' and brand == 'Hermes':
                    image_urls.add(url)
                elif 'balenciaga' in url and season == 'fall' and brand == 'Balenciaga':
                    image_urls.add(url)
                elif '_MON' in url and brand in ('Balmain', 'Celine', 'Prada'):
                    image_urls.add(url)
                elif 'DIO_' in url and season == 'spring' and brand == 'Dior':
                    image_urls.add(url)
                elif 'MARC' in url and season == 'spring' and brand in ('Isabel Marant', 'Loewe', 'Valentino'):
                    image_urls.add(url)
                elif 'MARC' in url and season == 'fall' and brand == 'Missoni':
                    image_urls.add(url)
                elif 'MIS_' in url and season == 'spring' and brand == 'Missoni':
                    image_urls.add(url)
                elif 'loewe' in url and season == 'fall' and brand == 'Loewe':
                    image_urls.add(url)
                elif 'dior' in url and season == 'fall' and brand == 'Dior':
                    image_urls.add(url)
                elif 'givenchy' in url and season == 'fall' and brand == 'Givenchy':
                    image_urls.add(url)
                elif 'AA2X' in url and season == 'spring' and brand == 'Christopher Kane':
                    image_urls.add(url)
                elif 'FEN_' in url and brand == 'Fendi':
                    image_urls.add(url)
                elif '_DOL' in url and brand == 'Dolce Gabbana':
                    image_urls.add(url)
                elif 'GUC_' in url and season == 'fall' and brand == 'Gucci':
                    image_urls.add(url)
                elif '_HER' in url and season == 'spring' and brand == 'Hermes':
                    image_urls.add(url)
                elif 'hermes' in url and season == 'fall' and brand == 'Hermes':
                    image_urls.add(url)
                elif 'valentino' in url and season == 'fall' and brand == 'Valentino':
                    image_urls.add(url)
                elif 'MAR' in url and season == 'spring' and brand in ('Alexander McQueen', 'Marni'):
                    image_urls.add(url)
                elif 'KOR' in url and season == 'spring' and brand == 'Michael Kors':
                    image_urls.add(url)
                elif 'ONP_' in url and season == 'fall' and brand == 'Michael Kors':
                    image_urls.add(url)
                elif 'alexander-mcqueen' in url and season == 'fall' and brand == 'Alexander McQueen':
                    image_urls.add(url)
                elif 'isabel-marant' in url and season == 'fall' and brand == 'Isabel Marant':
                    image_urls.add(url)
                elif 'MMM' in url and season == 'spring' and brand == 'Maison Margiela':
                    image_urls.add(url)
                elif 'maison-margiela' in url and season == 'fall' and brand == 'Maison Margiela':
                    image_urls.add(url)
                elif 'JWA_' in url and brand == 'J.W. Anderson':
                    image_urls.add(url)
                elif 'VUI_' in url and season == 'spring' and brand == 'Louis Vuitton':
                    image_urls.add(url)
                elif 'louis-vuitton' in url and season == 'fall' and brand == 'Louis Vuitton':
                    image_urls.add(url)
                elif 'CDG' in url and brand == 'Comme Des Garcons':
                    image_urls.add(url)
                elif '_DRI' in url and season == 'fall' and brand == 'Dries Van Noten':
                    image_urls.add(url)
                elif 'DVN_' in url and season == 'spring' and brand in ('Dries Van Noten'):
                    image_urls.add(url)
                elif '_ARC' in url and season == 'spring' and brand in ('Gucci'):
                    image_urls.add(url)
                elif '_A2X' in url and season == 'fall' and brand in ('Marc Jacobs', 'Tory Burch'):
                    image_urls.add(url)
                elif '_A2X' in url and season == 'spring' and brand in ('Saint Laurent'):
                    image_urls.add(url)
                elif 'saint-laurent' in url and season == 'fall' and brand == 'Saint Laurent':
                    image_urls.add(url)
                elif 'AA2X' in url and season == 'spring' and brand in ('Marc Jacobs', 'Tory Burch'):
                    image_urls.add(url)
                elif '_17G0' in url and season == 'spring' and brand in ('Miu Miu'):
                    image_urls.add(url)
                elif 'miu-miu' in url and season == 'fall' and brand in ('Miu Miu'):
                    image_urls.add(url)
