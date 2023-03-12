# https://realpython.com/beautiful-soup-web-scraper-python/
# Modul requests (pip install requests)
import requests
# Import knihovny BeautifulSoup4 (pip install beautifulsoup4), která usnadňuje web scraping
from bs4 import BeautifulSoup
import json

# Konstanta obsahující adresu webu, z něhož chceme získávat data
# Žebříček 100 knížek, které by měl každý přečíst podle serveru databazekhin.cz
URL = 'https://www.databazeknih.cz/seznamy/100-knizek-ktere-by-mel-kazdy-precist-70'

# Odeslání požadavku metodou get na určenou URL adresu - HTTP server vrací zpět obsah stránky
page = requests.get(URL)
# Vytvoření objektu parseru stránky
soup = BeautifulSoup(page.content, 'html.parser')
knihatitle = soup.select('.bigger')
knihalink = soup.select('.pozn')
# Získání názvů knih
titles = [tag.text for tag in knihatitle]
# Získání roku knih
years = [int(tag.text[:4]) for tag in knihalink]
# Získání autora knih
authors = [tag.text[6:] for tag in knihalink]

# Zapsaní dat do books.json
with open("books.json", "w", encoding='utf-8') as file:
    # zapsaní [ na začátku souboru
    file.write('[')
    for i in range(0, 30):
        # uloží do konstanty row data
        row = f'"title": "{titles[i]}", "year": "{years[i]}", "author": "{authors[i]}"'
        if i == 29:
            row = '{' + row + '} '
        # poslední řádek bude odřádkován
        else:
            row = '{' + row + '}, \n'

        # vypsaní row do konzole
        print(row)
        # zapsaní row do souboru
        file.write(row)

    # zapsaní ] na konci souboru
    file.write(']')