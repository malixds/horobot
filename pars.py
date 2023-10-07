import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


URL_TEMPLATE = 'https://74.ru/horoscope/daily/'
r = requests.get(URL_TEMPLATE)
soup = bs(r.text, "html.parser")
horo_divs = soup.find_all('article', 'IGRa5')

names = []
tmp = 1
dct = {}
# print('soup', soup)
for i in horo_divs:
    h3 = i.find('h3')
    # print(h3.text)
    p = i.find('div', 'BDPZt KUbeq')
    # print(p.text)
    dct[h3.text] = p.text

print(r.status_code)