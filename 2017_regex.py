match = re.match(r'.*(http.*(?:MAR|UMB|KIM|ALT|ARC|ALE|L7A|MON|BOT|CHA|DIO|CDG|DOL|FEN|VAL|GUC|HER|AG|WAT|MAR|KOR|KEN|STE|GIA|KAT|JUN|ROK|TEN|YSL|LUC|VET|WAN|LLL).*jpg).*', l)
            # match = re.match(r'.*(.*http:.*_MAR.*jpg.*).*', l)
            # match = re.match(r'.*(http:.*/_(?!ARC|AG|UMB|A2X|GAS|MIC).*.jpg).*', l)
            # match = re.match(r'.*(http:\/\/assets.vogue.com\/photos\/.*\/master\/pass\/.*.[jpg|JPG]).*', l)
            if match:
                url = match.group(1)

                if '_UMB' in url and season == 'spring' and brand in ('Valentino', 'Acne Studios', 'Loewe', 'Marc Jacobs', 'Oscar de la Renta'):
                    image_urls.add(url)
                elif 'KIM' in url and season == 'spring' and brand in ('Alexander McQueen', 'Antonio Berardi', 'Christopher Kane', 'Marc Jacobs', 'Louis Vuitton', 'Isabel Marant', 'Dries Van Noten', 'Kenzo', 'Lanvin', 'Mary Katrantzou', 'Missoni'):
                    image_urls.add(url)
                elif '_ALE' in url and season == 'spring' and brand == 'Alexander Wang':
                    image_urls.add(url)
                elif '_ALT' in url and season == 'spring' and brand == 'Altuzarra':
                    image_urls.add(url)
                elif '_L7A' in url and season == 'spring' and brand == 'Ann Demeulemeester':
                    image_urls.add(url)
                elif '_MON' in url and season == 'spring' and brand in ('Balenciaga', 'Balmain', 'Celine', 'Givenchy', 'Miu Miu', 'Prada', 'Proenza Schouler'):
                    image_urls.add(url)
                elif '_BOT' in url and season == 'spring' and brand == 'Bottega Veneta':
                    image_urls.add(url)
                elif '_CHA' in url and brand == 'Chanel':
                    image_urls.add(url)
                elif '_DIO' in url and brand == 'Christian Dior':
                    image_urls.add(url)
                elif '_CDG' in url and season == 'spring' and brand == 'Comme Des Garcons':
                    image_urls.add(url)
                elif '_DOL' in url and brand == 'Dolce Gabbana':
                    image_urls.add(url)
                elif '_FEN' in url and season == 'spring' and brand == 'Fendi':
                    image_urls.add(url)
                elif '_VAL' in url and season == 'spring' and brand == 'Giambattista Valli':
                    image_urls.add(url)
                elif '_GUC' in url and brand == 'Gucci':
                    image_urls.add(url)
                elif '_HER' in url and brand == 'Hermes':
                    image_urls.add(url)
                elif '_AG' in url and season == 'spring' and brand == 'J.W. Anderson':
                    image_urls.add(url)
                elif '_WAT' in url and season == 'spring' and brand == 'Junya Watanabe':
                    image_urls.add(url)
                elif '_MAR' in url and season == 'spring' and brand in ('Maison Margiela', 'Marni'):
                    image_urls.add(url)
                elif '_KOR' in url and brand == 'Michael Kors':
                    image_urls.add(url)
                elif '_LUC' in url and season == 'spring' and brand in ('Tory Burch', 'Roksanda'):
                    image_urls.add(url)
                elif '_STE' in url and season == 'spring' and brand == 'Stella McCartney':
                    image_urls.add(url)
                elif '_YSL' in url and brand == 'Saint Laurent':
                    image_urls.add(url)
                elif '_VET' in url and season == 'spring' and brand == 'Vetements':
                    image_urls.add(url)
                elif '_UMB' in url and season == 'fall' and brand in ('Acne Studios', 'Altuzarra', 'Isabel Marant', 'Louis Vuitton', 'Marc Jacobs', 'Stella McCartney'):
                    image_urls.add(url)
                elif 'KIM' in url and season == 'fall' and brand in ('Alexander McQueen', 'Christopher Kane', 'Antonio Berardi', 'Comme Des Garcons', 'Dries Van Noten', 'Fendi', 'J.W. Anderson', 'Lanvin', 'Loewe'):
                    image_urls.add(url)
                elif '_WAN' in url and season == 'fall' and brand == 'Alexander Wang':
                    image_urls.add(url)
                elif '_LLL' in url and season == 'fall' and brand == 'Ann Demeulemeester':
                    image_urls.add(url)
                elif '_MON' in url and season == 'fall' and brand in ('Balenciaga', 'Balmain', 'Celine', 'Miu Miu', 'Prada', 'Proenza Schouler'):
                    image_urls.add(url)
                elif '_GIA' in url and season == 'fall' and brand == 'Giambattista Valli':
                    image_urls.add(url)
                elif '_KEN' in url and season == 'fall' and brand == 'Kenzo':
                    image_urls.add(url)
                elif '_MAR' in url and season == 'fall' and brand in ('Marni', 'Maison Margiela'):
                    image_urls.add(url)
                elif '_KAT' in url and season == 'fall' and brand == 'Mary Katrantzou':
                    image_urls.add(url)
                elif '_ROK' in url and season == 'fall' and brand == 'Roksanda':
                    image_urls.add(url)
                elif '_TEN' in url and season == 'fall' and brand == 'Oscar de la Renta':
                    image_urls.add(url)
                elif '_ARC' in url and season == 'fall' and brand in ('Missoni', 'Tory Burch', 'Vetements'):
                    image_urls.add(url)
                elif '_VAL' in url and season == 'fall' and brand == 'Valentino':
                    image_urls.add(url)
